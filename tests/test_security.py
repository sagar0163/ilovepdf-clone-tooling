"""Regression tests for issue #7: path traversal / arbitrary file write in upload handlers."""
import io
import shutil
from pathlib import Path
from unittest import mock

import pytest
from fastapi import UploadFile
from fastapi.testclient import TestClient

from ilovepdf import file_ops
from ilovepdf import main, compress, split, watermark, merge

TRAVERSAL_NAMES = [
    "../../../tmp/pwned.pdf",
    "..\\..\\tmp\\pwned.pdf",
    "uploads/../../../etc/cron.d/evil",
]

SIMPLE_PDF = b"%PDF-1.4 fake content for traversal tests, not a real PDF"


@pytest.fixture(autouse=True)
def clean_work_dirs():
    for d in (main.UPLOAD_DIR, main.OUTPUT_DIR):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)
    yield
    for d in (main.UPLOAD_DIR, main.OUTPUT_DIR):
        if d.exists():
            shutil.rmtree(d)


def _client():
    return TestClient(main.app)


def _merge_request(client, filename):
    return client.post(
        "/merge",
        files=[("files", (filename, io.BytesIO(SIMPLE_PDF), "application/pdf"))],
    )


def test_filename_with_traversal_never_escapes_uploads_dir():
    recorded = {}

    def fake_merge(inputs, output_path):
        recorded["input"] = inputs
        Path(output_path).write_bytes(SIMPLE_PDF)
        return True

    with mock.patch("ilovepdf.merge.merge_pdfs", side_effect=fake_merge):
        resp = _merge_request(_client(), "/../../../tmp/pwned.pdf")

    assert resp.status_code == 200
    written = Path(recorded["input"][0])
    assert written.resolve().is_relative_to(main.UPLOAD_DIR.resolve())
    assert written.name == "pwned.pdf"
    assert not (Path("/tmp") / "pwned.pdf").exists()


@pytest.mark.parametrize("crafted", TRAVERSAL_NAMES)
def test_save_upload_sanitizes_or_rejects_crafted_uploadfile_filename(tmp_path, crafted):
    upload = UploadFile(filename=crafted, file=io.BytesIO(SIMPLE_PDF))
    if "\\" in crafted:
        with pytest.raises(ValueError):
            file_ops.save_upload(upload.filename, upload.file, tmp_path)
        return
    target = file_ops.save_upload(upload.filename, upload.file, tmp_path)
    assert target.parent == tmp_path
    assert target.is_relative_to(tmp_path)
    assert ".." not in target.parts
    assert "\\" not in target.name and "/" not in target.name


@pytest.mark.parametrize("bad", [".", "..", "..\\..\\evil", "/", "\\", ""])
def test_safe_filename_rejects_traversal_tokens(bad):
    with pytest.raises(ValueError):
        file_ops.safe_filename(bad)


def test_merge_requests_get_isolated_output_dirs():
    calls = []

    def fake_merge(inputs, output_path):
        marker = b"result-%d" % (len(calls) + 1)
        calls.append((str(output_path), marker))
        Path(output_path).write_bytes(marker)
        return True

    with mock.patch("ilovepdf.merge.merge_pdfs", side_effect=fake_merge):
        client = _client()
        r1 = _merge_request(client, "first.pdf")
        r2 = _merge_request(client, "second.pdf")

    assert r1.status_code == r2.status_code == 200
    assert r1.content == b"result-1"
    assert r2.content == b"result-2"
    assert len(calls) == 2
    out_paths = [Path(p) for p, _ in calls]
    assert len({str(p) for p in out_paths}) == 2
    for p in out_paths:
        assert p.resolve().is_relative_to(main.OUTPUT_DIR.resolve())


def test_symlink_at_fixed_output_name_cannot_be_overwritten(tmp_path):
    victim = tmp_path / "victim.txt"
    victim.write_text("precious data")
    symlink = main.OUTPUT_DIR / "merged.pdf"
    symlink.symlink_to(victim)

    def fake_merge(inputs, output_path):
        Path(output_path).write_bytes(SIMPLE_PDF)
        return True

    with mock.patch("ilovepdf.merge.merge_pdfs", side_effect=fake_merge):
        resp = _merge_request(_client(), "attack.pdf")

    assert resp.status_code == 200
    assert resp.content == SIMPLE_PDF
    assert victim.read_text() == "precious data"
    assert symlink.is_symlink()


def test_temp_files_removed_after_response():
    def fake_merge(inputs, output_path):
        Path(output_path).write_bytes(SIMPLE_PDF)
        return True

    with mock.patch("ilovepdf.merge.merge_pdfs", side_effect=fake_merge):
        resp = _merge_request(_client(), "cleanup.pdf")

    assert resp.status_code == 200
    assert list(main.UPLOAD_DIR.iterdir()) == []
    assert list(main.OUTPUT_DIR.iterdir()) == []


def test_split_fix_and_per_request_cleanup():
    with mock.patch("ilovepdf.split.split_pdf", return_value=["page_1.pdf", "page_2.pdf"]):
        resp = _client().post(
            "/split",
            files=[("file", ("report.pdf", io.BytesIO(SIMPLE_PDF), "application/pdf"))],
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["pages"] == 2
    assert Path(data["output_dir"]).resolve().is_relative_to(main.OUTPUT_DIR.resolve())
    assert list(main.UPLOAD_DIR.iterdir()) == []
    assert list(main.OUTPUT_DIR.iterdir()) == []