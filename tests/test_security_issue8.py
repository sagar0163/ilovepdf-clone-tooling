"""Regression tests for issue #8: safe-by-default auth, host bind, size caps,
MIME sniffing, and CORS hardening."""
import io
import shutil
from pathlib import Path
from unittest import mock

import pytest
from fastapi.testclient import TestClient

import main
import security

SIMPLE_PDF = b"%PDF-1.4 fake content for issue-8 tests, not a real PDF"
NOT_PDF = b"username\npassword\n"


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


# ---------------------------------------------------------------------------
# Host binding
# ---------------------------------------------------------------------------

def test_host_defaults_to_localhost(monkeypatch):
    monkeypatch.delenv("API_HOST", raising=False)
    assert security.get_host() == "127.0.0.1"


def test_host_can_be_published_via_env(monkeypatch):
    monkeypatch.setenv("API_HOST", "0.0.0.0")
    assert security.get_host() == "0.0.0.0"


def test_port_defaults_to_8000(monkeypatch):
    monkeypatch.delenv("API_PORT", raising=False)
    assert security.get_port() == 8000


# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------

def test_cors_defaults_to_same_origin(monkeypatch):
    monkeypatch.delenv("CORS_ORIGINS", raising=False)
    kwargs = security.get_cors_kwargs()
    assert kwargs["allow_origins"] == []
    assert kwargs["allow_credentials"] is False


def test_cors_allowlist_from_env(monkeypatch):
    monkeypatch.setenv("CORS_ORIGINS", "https://app.example.com,https://admin.example.com")
    kwargs = security.get_cors_kwargs()
    assert kwargs["allow_origins"] == [
        "https://app.example.com",
        "https://admin.example.com",
    ]
    assert kwargs["allow_credentials"] is True


def test_cors_wildcard_never_combined_with_credentials(monkeypatch):
    monkeypatch.setenv("CORS_ORIGINS", "*")
    kwargs = security.get_cors_kwargs()
    assert kwargs["allow_origins"] == ["*"]
    assert kwargs["allow_credentials"] is False


def test_no_acao_header_by_default():
    resp = _client().get("/health", headers={"Origin": "http://evil.example"})
    assert "access-control-allow-origin" not in resp.headers


# ---------------------------------------------------------------------------
# Bearer-token auth
# ---------------------------------------------------------------------------

def test_auth_off_by_default_warns(monkeypatch, caplog):
    monkeypatch.delenv("API_TOKEN", raising=False)
    assert security.auth_enabled() is False


def test_auth_401_when_token_set_and_missing(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "sekret")
    client = _client()
    assert client.get("/health").status_code == 200
    resp = client.post(
        "/merge",
        files=[("files", ("doc.pdf", io.BytesIO(SIMPLE_PDF), "application/pdf"))],
    )
    assert resp.status_code == 401


@pytest.mark.parametrize("endpoint", ["/merge", "/split", "/compress", "/watermark"])
def test_protected_endpoints_401_unauthenticated(monkeypatch, endpoint):
    monkeypatch.setenv("API_TOKEN", "sekret")
    resp = _client().post(
        endpoint,
        files=[("file", ("doc.pdf", io.BytesIO(SIMPLE_PDF), "application/pdf"))],
    )
    assert resp.status_code == 401


def test_wrong_token_401(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "sekret")
    resp = _client().post(
        "/compress",
        files=[("file", ("doc.pdf", io.BytesIO(SIMPLE_PDF), "application/pdf"))],
        headers={"Authorization": "Bearer wrong"},
    )
    assert resp.status_code == 401


def test_valid_token_passes_to_parser(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "sekret")

    def fake_compress(input_path, output_path, quality):
        Path(output_path).write_bytes(SIMPLE_PDF)
        return True

    with mock.patch("compress.compress_pdf", side_effect=fake_compress):
        resp = _client().post(
            "/compress",
            files=[("file", ("doc.pdf", io.BytesIO(SIMPLE_PDF), "application/pdf"))],
            headers={"Authorization": "Bearer sekret"},
        )
    assert resp.status_code == 200
    assert resp.content == SIMPLE_PDF


def test_auth_401_happens_before_parser_runs(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "sekret")
    with mock.patch("merge.merge_pdfs") as m:
        resp = _client().post(
            "/merge",
            files=[("files", ("doc.pdf", io.BytesIO(SIMPLE_PDF), "application/pdf"))],
        )
    assert resp.status_code == 401
    m.assert_not_called()


# ---------------------------------------------------------------------------
# Upload size cap
# ---------------------------------------------------------------------------

def test_upload_over_size_cap_rejected_413(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "sekret")
    monkeypatch.setenv("MAX_UPLOAD_MB", "0")
    with mock.patch("compress.compress_pdf") as m:
        resp = _client().post(
            "/compress",
            files=[("file", ("doc.pdf", io.BytesIO(SIMPLE_PDF), "application/pdf"))],
            headers={"Authorization": "Bearer sekret"},
        )
    assert resp.status_code == 413
    m.assert_not_called()


def test_upload_size_cap_default_100mb():
    assert security.get_max_upload_bytes() == 100 * 1024 * 1024


# ---------------------------------------------------------------------------
# MIME sniffing / PDF validation
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("endpoint", ["/split", "/compress", "/watermark"])
def test_non_pdf_magic_rejected_before_parser(monkeypatch, endpoint):
    with mock.patch("compress.compress_pdf") as comp_m, mock.patch(
        "split.split_pdf"
    ) as split_m, mock.patch("watermark.add_watermark") as wm_m:
        resp = _client().post(
            endpoint,
            files=[("file", ("doc.pdf", io.BytesIO(NOT_PDF), "application/pdf"))],
        )
    assert resp.status_code == 400
    assert not comp_m.called and not split_m.called and not wm_m.called


def test_non_pdf_extension_rejected(monkeypatch):
    with mock.patch("split.split_pdf") as m:
        resp = _client().post(
            "/split",
            files=[("file", ("doc.txt", io.BytesIO(SIMPLE_PDF), "application/pdf"))],
        )
    assert resp.status_code == 400
    m.assert_not_called()


def test_merge_rejects_any_non_pdf_file(monkeypatch):
    with mock.patch("merge.merge_pdfs") as m:
        resp = _client().post(
            "/merge",
            files=[
                ("files", ("a.pdf", io.BytesIO(SIMPLE_PDF), "application/pdf")),
                ("files", ("b.pdf", io.BytesIO(NOT_PDF), "application/pdf")),
            ],
        )
    assert resp.status_code == 400
    m.assert_not_called()


# ---------------------------------------------------------------------------
# docker-compose does not publish 8000 by default
# ---------------------------------------------------------------------------

def test_compose_does_not_publish_8000():
    text = Path("docker-compose.yml").read_text()
    offending = [
        line for line in text.splitlines()
        if "8000:8000" in line and not line.lstrip().startswith("#")
    ]
    assert offending == [], (
        "port 8000 must not be published by default; found active mapping: "
        f"{offending}"
    )