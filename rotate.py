"""Page Rotation Tool - Rotate PDF pages by specified angle"""


def rotate_pages(input_path, output_path, angle=90, pages=None):
    """
    Rotate pages in PDF by specified angle.
    
    Args:
        input_path: Path to input PDF
        output_path: Path for rotated PDF
        angle: Rotation angle (90, 180, 270)
        pages: List of page indices to rotate (None = all pages)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        for i, page in enumerate(reader.pages):
            if pages is None or i in pages:
                page.rotate(angle)
            writer.add_page(page)
        
        with open(output_path, "wb") as f:
            writer.write(f)
        
        return True
    except Exception as e:
        print(f"Error rotating pages: {e}")
        return False


if __name__ == "__main__":
    rotate_pages("input.pdf", "rotated.pdf", angle=90)

