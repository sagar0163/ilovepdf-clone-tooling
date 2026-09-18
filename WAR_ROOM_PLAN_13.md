# Plan for Issue #13: Real PDF Compression

- [ ] Create a test PDF with a large embedded image to verify compression.
- [ ] Implement Ghostscript-based compression in `compress.py` mapping `quality` to `-dPDFSETTINGS`.
- [ ] Update `compress_pdf` signature/docstrings to document text-only vs image-heavy behavior.
- [ ] Verify byte size reduction is ~40% for `quality="medium"`.
- [ ] Ensure `compress_pdf` returns correct output path and handles exceptions.
- [ ] Update `compress` endpoint in `main.py` and CLI to reflect improvements if needed.
- [ ] Verify test PDF opens correctly and page counts match (using PyPDF2).
