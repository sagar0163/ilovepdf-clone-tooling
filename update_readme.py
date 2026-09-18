import re

with open('README.md', 'r') as f:
    content = f.read()

# Replace Installation section
new_install = """## 🚀 Installation

### Quick Install (Editable mode)

```bash
pip install -e .
```

This installs the package and the `ilovepdf` command-line tool.
"""
content = re.sub(r'## 🚀 Installation.*?---', new_install + '\n---', content, flags=re.DOTALL)

# Add Quick start (CLI)
quick_start = """## ⚡ Quick start (CLI)

The `ilovepdf` CLI provides access to the PDF tools directly from your terminal:

```bash
# List all available commands
ilovepdf --help

# Merge PDFs
ilovepdf merge file1.pdf file2.pdf -o merged.pdf

# Split a PDF into pages
ilovepdf split doc.pdf -o pages/

# Compress a PDF
ilovepdf compress in.pdf -o out.pdf --quality medium
```
"""

# Replace Usage section with Quick Start and Python API
content = re.sub(r'## 💻 Usage', quick_start + '\n---\n\n## 💻 Python API Usage', content)

# Remove the old Command Line Usage
content = re.sub(r'## 🔧 Command Line Usage.*?---', '', content, flags=re.DOTALL)

# Update Project Structure
new_structure = """## 📁 Project Structure

```
ilovepdf-clone-tooling/
├── pyproject.toml     # Package configuration
├── src/
│   └── ilovepdf/      # Package source code
│       ├── cli.py     # CLI entry point
│       ├── merge.py   # PDF merger module
│       ├── split.py   # PDF splitter module
│       ├── compress.py# PDF compressor
│       └── ...        # Other modules
└── ...
```
"""
content = re.sub(r'## 📁 Project Structure.*?---', new_structure + '\n---', content, flags=re.DOTALL)

# Update the code examples in Python API Usage to import from ilovepdf
content = re.sub(r'from merge import', 'from ilovepdf.merge import', content)
content = re.sub(r'from split import', 'from ilovepdf.split import', content)
content = re.sub(r'from compress import', 'from ilovepdf.compress import', content)
content = re.sub(r'from pdf_to_word import', 'from ilovepdf.pdf_to_word import', content)
content = re.sub(r'from img_to_pdf import', 'from ilovepdf.img_to_pdf import', content)
content = re.sub(r'from watermark import', 'from ilovepdf.watermark import', content)
content = re.sub(r'from protect import', 'from ilovepdf.protect import', content)
content = re.sub(r'from unlock import', 'from ilovepdf.unlock import', content)
content = re.sub(r'from rotate import', 'from ilovepdf.rotate import', content)


with open('README.md', 'w') as f:
    f.write(content)
