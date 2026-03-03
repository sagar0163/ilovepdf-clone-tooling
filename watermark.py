"""Watermark Tool - Add text or image watermarks to PDF"""


def add_watermark(input_path, output_path, text=None, image_path=None, opacity=0.3):
    """
    Add watermark to PDF pages.
    
    Args:
        input_path: Path to input PDF
        output_path: Path for watermarked PDF
        text: Text to use as watermark
        image_path: Image to use as watermark
        opacity: Watermark opacity (0-1)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        import io
        
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        for page in reader.pages:
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
            writer.add_page(page)
        
        with open(output_path, "wb") as f:
            writer.write(f)
        
        return True
    except Exception as e:
        print(f"Error adding watermark: {e}")
        return False


if __name__ == "__main__":
    add_watermark("input.pdf", "watermarked.pdf", text="CONFIDENTIAL")

