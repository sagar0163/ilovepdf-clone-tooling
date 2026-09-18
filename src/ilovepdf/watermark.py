"""Watermark Tool - Add text or image watermarks to PDF"""

import io
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from core import _copy_pdf

def add_watermark(input_path, output_path, text=None, image_path=None, opacity=0.3):
    """
    Add watermark to PDF pages.
    """
    def page_transform(i, page):
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=letter)
        
        if text:
            c.setFillColorRGB(0.5, 0.5, 0.5, alpha=opacity)
            c.saveState()
            c.translate(200, 400)
            c.rotate(45)
            c.drawString(0, 0, text)
            c.restoreState()
        
        c.save()
        packet.seek(0)
        
        watermark = PdfReader(packet)
        page.merge_page(watermark.pages[0])

    out = _copy_pdf(input_path, output_path, page_transform=page_transform)
    return str(out)

if __name__ == "__main__":
    try:
        add_watermark("input.pdf", "watermarked.pdf", text="CONFIDENTIAL")
    except Exception as e:
        print(f"Error adding watermark: {e}")
