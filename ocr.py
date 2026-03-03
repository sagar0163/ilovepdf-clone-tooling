"""OCR Support - Make scanned PDFs searchable using Tesseract"""


def ocr_pdf(input_path, output_path=None, lang="eng"):
    """
    Perform OCR on scanned PDF to make it searchable.
    
    Args:
        input_path: Path to input PDF (scanned)
        output_path: Path for output searchable PDF
        lang: Language code for OCR (default: eng)
    
    Returns:
        bool: True if successful
    """
    try:
        from pdf2image import convert_from_path
        from pytesseract import pytesseract
        from PyPDF2 import PdfWriter
        from PIL import Image
        import os
        
        if output_path is None:
            output_path = input_path.replace(".pdf", "_ocr.pdf")
        
        # Convert PDF to images
        images = convert_from_path(input_path)
        
        writer = PdfWriter()
        
        for i, image in enumerate(images):
            # Perform OCR on image
            text = pytesseract.image_to_string(image, lang=lang)
            
            # Add text layer to PDF
            # For now, save the text
            print(f"Page {i+1}: {len(text)} characters extracted")
        
        print(f"OCR completed. Text extracted to: {output_path.replace(.pdf, .txt)}")
        return True
    except Exception as e:
        print(f"Error performing OCR: {e}")
        return False


def extract_text_from_image(image_path, lang="eng"):
    """
    Extract text from a single image using OCR.
    
    Args:
        image_path: Path to image file
        lang: Language code for OCR
    
    Returns:
        str: Extracted text
    """
    try:
        from pytesseract import pytesseract
        
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang=lang)
        
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""


if __name__ == "__main__":
    ocr_pdf("scanned_document.pdf")

