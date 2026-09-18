"""Page Rotation Tool - Rotate PDF pages by specified angle"""

from ilovepdf.core import _copy_pdf

def rotate_pages(input_path, output_path, angle=90, pages=None):
    """
    Rotate pages in PDF by specified angle.
    """
    def page_transform(i, page):
        if pages is None or i in pages:
            page.rotate(angle)
            
    out = _copy_pdf(input_path, output_path, page_transform=page_transform)
    return str(out)

if __name__ == "__main__":
    try:
        rotate_pages("input.pdf", "rotated.pdf", angle=90)
    except Exception as e:
        print(f"Error rotating pages: {e}")
