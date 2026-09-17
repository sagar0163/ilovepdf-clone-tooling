"""Safe-by-default security primitives for the PDF API.

Env vars:
    API_HOST        – bind address (default 127.0.0.1; set to 0.0.0.0 to
                      expose publicly — operator must opt-in).
    API_PORT        – port (default 8000).
    API_TOKEN       – optional bearer token; when set, every mutating
                      endpoint requires ``Authorization: Bearer <token>``.
    CORS_ORIGINS    – comma-separated list of allowed origins.  When unset
                      no CORS headers are sent (same-origin default).
    MAX_UPLOAD_MB   – per-file upload cap in MiB (default 100).
"""

from __future__ import annotations

import logging
import os
import secrets
from typing import Optional

from fastapi import Depends, Header, HTTPException, Request, UploadFile

logger = logging.getLogger("security")

# ---------------------------------------------------------------------------
# Host / port
# ---------------------------------------------------------------------------

def get_host() -> str:
    """Return the bind host.  ``127.0.0.1`` unless ``API_HOST`` is set."""
    host = os.environ.get("API_HOST", "127.0.0.1")
    if host == "127.0.0.1":
        logger.info("API_HOST not set — binding to 127.0.0.1 (localhost only)")
    return host


def get_port() -> int:
    return int(os.environ.get("API_PORT", "8000"))


# ---------------------------------------------------------------------------
# Bearer-token auth
# ---------------------------------------------------------------------------

def _get_expected_token() -> Optional[str]:
    return os.environ.get("API_TOKEN")


def auth_enabled() -> bool:
    """True when an API_TOKEN is configured (auth is on)."""
    return bool(os.environ.get("API_TOKEN"))


def verify_token(authorization: Optional[str] = Header(None)):
    """FastAPI dependency – enforces bearer auth when API_TOKEN is set."""
    expected = _get_expected_token()
    if expected is None:
        return
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing API token")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not secrets.compare_digest(token, expected):
        raise HTTPException(status_code=401, detail="Invalid API token")


# ---------------------------------------------------------------------------
# CORS config
# ---------------------------------------------------------------------------

def get_cors_kwargs() -> dict:
    """Build CORSMiddleware kwargs from env.

    Default: no origins (same-origin).  ``CORS_ORIGINS`` sets an explicit
    allowlist.  The wildcard ``*`` is **never** combined with credentials.
    """
    raw = os.environ.get("CORS_ORIGINS", "").strip()
    if not raw:
        return {
            "allow_origins": [],
            "allow_credentials": False,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        }
    origins = [o.strip() for o in raw.split(",") if o.strip()]
    if "*" in origins:
        logger.warning(
            "CORS_ORIGINS contains '*'; allow_credentials forced to False"
        )
        return {
            "allow_origins": ["*"],
            "allow_credentials": False,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        }
    return {
        "allow_origins": origins,
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }


# ---------------------------------------------------------------------------
# Upload size cap
# ---------------------------------------------------------------------------

def get_max_upload_bytes() -> int:
    mb = int(os.environ.get("MAX_UPLOAD_MB", "100"))
    return mb * 1024 * 1024


# ---------------------------------------------------------------------------
# PDF content validation
# ---------------------------------------------------------------------------

PDF_MAGIC = b"%PDF-"
PDF_EXTENSIONS = {".pdf"}


def validate_pdf_upload(file: UploadFile) -> None:
    """Reject uploads that are obviously not PDFs.

    Checks the file extension **and** the first bytes (magic number).
    Raises 400 before any parser sees the content.
    """
    if file.filename is not None:
        ext = _lower_ext(file.filename)
        if ext not in PDF_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Rejected: file extension '{ext}' is not a PDF",
            )

    head = file.file.read(8)
    file.file.seek(0)

    if not head.startswith(PDF_MAGIC):
        raise HTTPException(
            status_code=400,
            detail="Rejected: uploaded file does not start with %PDF- magic bytes",
        )


def _lower_ext(filename: str) -> str:
    idx = filename.rfind(".")
    if idx == -1:
        return ""
    return filename[idx:].lower()
