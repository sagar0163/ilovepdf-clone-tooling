"""PDF Splitter Module - Split PDF into individual pages"""

from core import _split_pdf

def split_pdf(input_file, output_dir):
    """
    Split a PDF into individual pages.
    
    Args:
        input_file: Path to input PDF
        output_dir: Directory to save split pages
    
    Returns:
        list: List of output file paths
    """
    # Simply call the core function; it raises exceptions on failure.
    paths = _split_pdf(input_file, output_dir)
    return [str(p) for p in paths]

if __name__ == "__main__":
    try:
        paths = split_pdf("input.pdf", "output_pages")
        print(f"Successfully split into {len(paths)} pages")
    except Exception as e:
        print(f"Error splitting PDF: {e}")
