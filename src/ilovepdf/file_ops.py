"""Secure filesystem helpers for the API.

Client-supplied filenames are never trusted: any directory components and
traversal tokens are stripped, and every request gets its own UUID-scoped
directory so request N can never read or clobber request M's files.
"""
import shutil
from pathlib import Path
from uuid import uuid4

FORBIDDEN_NAMES = frozenset({".", ".."})


def safe_filename(raw):
    """Return a path-safe basename for a client-supplied filename.

    Strips any directory components and rejects names that could escape the
    sandbox, including Windows-style separators and traversal tokens.
    """
    if not isinstance(raw, str) or not raw:
        raise ValueError("filename must be a non-empty string")

    name = Path(raw).name
    name = name.replace("\x00", "").strip()

    if not name or name in FORBIDDEN_NAMES:
        raise ValueError("invalid filename")
    if "/" in name or "\\" in name:
        raise ValueError("filename must not contain path separators")

    return name


def new_request_dir(base):
    """Create a fresh, unpredictable directory inside ``base`` and return it."""
    req_dir = base / uuid4().hex
    req_dir.mkdir(parents=True, exist_ok=False)
    return req_dir


def save_upload(filename, fileobj, dest_dir):
    """Write ``fileobj`` to ``dest_dir`` under a sanitized basename.

    Returns the resulting Path. The write can never leave ``dest_dir`` because
    the name is reduced to its basename first.
    """
    target = dest_dir / safe_filename(filename)
    with target.open("wb") as buffer:
        shutil.copyfileobj(fileobj, buffer)
    return target


def unique_output_path(base, name):
    """Return a path ``base/<uuid>/<sanitized-name>`` for request-scoped output."""
    return new_request_dir(base) / safe_filename(name)


def cleanup_path(path):
    """Best-effort removal of a per-request file or directory."""
    try:
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path, ignore_errors=True)
        else:
            path.unlink(missing_ok=True)
    except OSError:
        pass