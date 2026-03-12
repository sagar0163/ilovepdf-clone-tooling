# iLovePDF Clone Tooling

A comprehensive collection of PDF manipulation scripts and tools for automated workflows. This toolkit provides professional-grade PDF operations including merge, split, compress, convert, watermark, and more.

![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)

---

## 📚 Features

| Tool | Description |
|------|-------------|
| 🔀 **Merge** | Combine multiple PDF files into one |
| ✂️ **Split** | Extract pages from PDF into separate files |
| 📦 **Compress** | Reduce PDF file size |
| 📝 **PDF to Word** | Convert PDF documents to Word (.docx) |
| 🖼️ **Image to PDF** | Convert images to PDF documents |
| 💧 **Watermark** | Add text or image watermarks |
| 🔒 **Protect** | Encrypt PDF with password |
| 🔓 **Unlock** | Remove password protection |
| 🔄 **Rotate** | Rotate PDF pages by any angle |

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Required Packages

```
PyPDF2>=3.0.0      # PDF manipulation
pdf2docx>=0.5.0    # PDF to Word conversion
reportlab>=4.0.0  # PDF generation
Pillow>=10.0.0    # Image processing
```

---

## 💻 Usage

### Merge PDFs

```python
from merge import merge_pdfs

# Merge multiple PDFs
files = ["file1.pdf", "file2.pdf", "file3.pdf"]
merge_pdfs(files, "merged_output.pdf")
```

### Split PDF

```python
from split import split_pdf

# Split PDF into individual pages
split_pdf("input.pdf", "output_directory")
```

### Compress PDF

```python
from compress import compress_pdf

# Compress with different quality levels
compress_pdf("large.pdf", "small.pdf", quality="medium")  # low, medium, high
```

### PDF to Word

```python
from pdf_to_word import convert_to_word

# Convert PDF to DOCX
convert_to_word("document.pdf", "document.docx")
```

### Image to PDF

```python
from img_to_pdf import convert_images_to_pdf

# Convert images to PDF
images = ["photo1.jpg", "photo2.jpg", "photo3.png"]
convert_images_to_pdf(images, "output.pdf")
```

### Add Watermark

```python
from watermark import add_watermark

# Add text watermark
add_watermark("input.pdf", "output.pdf", text="CONFIDENTIAL")

# Add image watermark
add_watermark("input.pdf", "output.pdf", image_path="logo.png", opacity=0.5)
```

### Protect PDF

```python
from protect import encrypt_pdf

# Encrypt PDF with password
encrypt_pdf("document.pdf", "protected.pdf", password="your_password")
```

### Unlock PDF

```python
from unlock import unlock_pdf

# Remove password protection
unlock_pdf("locked.pdf", "unlocked.pdf", password="your_password")
```

### Rotate Pages

```python
from rotate import rotate_pages

# Rotate all pages 90 degrees
rotate_pages("input.pdf", "rotated.pdf", angle=90)

# Rotate specific pages
rotate_pages("input.pdf", "rotated.pdf", angle=180, pages=[0, 2, 4])
```

---

## 📁 Project Structure

```
ilovepdf-clone-tooling/
├── merge.py           # PDF merger module
├── split.py          # PDF splitter module
├── compress.py        # PDF compressor
├── pdf_to_word.py    # PDF to Word converter
├── img_to_pdf.py     # Image to PDF converter
├── watermark.py      # Watermark tool
├── protect.py        # PDF encryption
├── unlock.py         # PDF decryption
├── rotate.py         # Page rotation
├── requirements.txt  # Python dependencies
├── API.md           # API documentation
└── README.md        # This file
```

---

## 🔧 Command Line Usage

You can also use these tools from the command line:

```bash
# Merge PDFs
python merge.py file1.pdf file2.pdf -o merged.pdf

# Split PDF
python split.py input.pdf -o output_dir/

# Compress PDF
python compress.py input.pdf -o compressed.pdf --quality high
```

---

## ⚠️ Error Handling

All modules include error handling. If an operation fails, the function returns `False` and prints an error message.

```python
from merge import merge_pdfs

result = merge_pdfs(files, "output.pdf")
if not result:
    print("Merge failed!")
```

---

## 📝 License

This project is licensed under the MIT License.

---

## 👤 Author

**Sagar Jadhav**
- GitHub: [@sagar0163](https://github.com/sagar0163)
- Twitter: [@sagarjadhav063](https://twitter.com/sagarjadhav063)

---

## 🙏 Acknowledgments

- [PyPDF2](https://github.com/py-pdf/PyPDF2) - Pure Python PDF library
- [pdf2docx](https://github.com/dothinking/pdf2docx) - PDF to Word converter
- [ReportLab](https://www.reportlab.com/) - PDF generation toolkit
- [Pillow](https://python-pillow.org/) - Python Imaging Library
# Updated
