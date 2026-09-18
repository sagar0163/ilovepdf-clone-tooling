import os
import tempfile
import pytest
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from compress import compress_pdf
from PyPDF2 import PdfReader

def create_large_pdf(path):
    # Create a large image to ensure it's compressible
    img = Image.new('RGB', (3000, 3000), color=(255, 255, 255))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    # Draw some large shapes
    for i in range(10):
        draw.rectangle([i*100, i*100, 3000-i*100, 3000-i*100], outline=(0, 0, 0), width=10)
        draw.ellipse([i*120, i*120, 3000-i*120, 3000-i*120], fill=(255, 0, 0))
    
    img_path = path + ".png"
    img.save(img_path, "PNG")
    
    c = canvas.Canvas(path, pagesize=A4)
    c.drawImage(img_path, 0, 0, width=A4[0], height=A4[1])
    c.showPage()
    c.save()
    os.remove(img_path)

def test_compress_pdf_medium():
    with tempfile.TemporaryDirectory() as tempdir:
        input_pdf = os.path.join(tempdir, "input.pdf")
        output_pdf = os.path.join(tempdir, "output.pdf")
        
        create_large_pdf(input_pdf)
        original_size = os.path.getsize(input_pdf)
        
        # Act
        result = compress_pdf(input_pdf, output_pdf, quality="medium")
        
        # Assert
        assert result == output_pdf
        assert os.path.exists(output_pdf)
        
        compressed_size = os.path.getsize(output_pdf)
        print(f"Original size: {original_size}, Compressed size: {compressed_size}")
        
        # At least 40% smaller
        assert compressed_size < original_size * 0.6
        
        # Check page count matches
        reader_in = PdfReader(input_pdf)
        reader_out = PdfReader(output_pdf)
        assert len(reader_in.pages) == len(reader_out.pages)

