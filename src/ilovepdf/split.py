"""PDF Splitter Module - Split PDF into individual pages"""

from ilovepdf.core import _split_pdf

def split_pdf(input_file, output_dir, on_progress=None):
    """
    Split a PDF into individual pages.
    """
    paths = _split_pdf(input_file, output_dir, on_page=on_progress)
    return [str(p) for p in paths]

if __name__ == "__main__":
    try:
        paths = split_pdf("input.pdf", "output_pages")
        print(f"Successfully split into {len(paths)} pages")
    except Exception as e:
        print(f"Error splitting PDF: {e}")
