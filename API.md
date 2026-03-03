# API Documentation

## PDF Tools API

### Merge PDFs
```python
from merge import merge_pdfs
merge_pdfs(["file1.pdf", "file2.pdf"], "merged.pdf")
```

### Split PDF
```python
from split import split_pdf
split_pdf("input.pdf", "output_dir")
```

### Compress PDF
```python
from compress import compress_pdf
compress_pdf("large.pdf", "small.pdf", quality="medium")
```

### Add Watermark
```python
from watermark import add_watermark
add_watermark("input.pdf", "output.pdf", text="CONFIDENTIAL")
```

