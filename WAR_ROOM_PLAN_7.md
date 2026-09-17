# War Room Plan — Issue #7: Security (path traversal / arbitrary file write)

## Staus: COMPLETE — all subtasks done, tests pass, ready to remove plan file and push.

- [x] Add secure file_ops helpers: `safe_filename`, per-request UUID dirs (`new_request_dir`), `save_upload`, `unique_output_path`, `cleanup_path` (commit 91fb3b6)
- [x] Harden all upload endpoints (/merge, /split, /compress, /watermark) in main.py: never join `UPLOAD_DIR / f.filename`; sanitize client filename + per-request UUID dirs; BackgroundTasks cleanup after response; split bugfix (commit a2a4ec4)
- [x] Add httpx + pytest to requirements for TestClient-based security tests (commit 8c86578)
- [x] Add security regression tests: path traversal can't escape uploads/, output-dir isolation for concurrent /merge, symlink-at-fixed-name can't be overwritten, temp file cleanup after response, split fix (commit 0b8602c)
- [x] Dockerfile hardening — run as non-root (appuser) to limit arbitrary-write blast radius (commit 643e326)
- [x] Regression test: filename `../../../tmp/pwned` never writes outside UPLOAD_DIR (tests/test_security.py::test_filename_with_traversal_never_escapes_uploads_dir)
- [x] Two simultaneous /merge requests each get isolated output dirs (test_merge_requests_get_isolated_output_dirs)
- [x] Symlink at fixed `output/merged.pdf` cannot be overwritten (test_symlink_at_fixed_output_name_cannot_be_overwritten)
- [x] Temp upload/output files removed after response (test_temp_files_removed_after_response, test_split_fix_and_per_request_cleanup)
- [x] Verify full security test suite passes: `pytest tests/test_security.py` → 14 passed
- [x] Remove this scratch plan file and make final commit referencing #7, then push branch