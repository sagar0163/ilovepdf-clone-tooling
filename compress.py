"""PDF Compressor Module - Reduce PDF file size"""


def compress_pdf(input_path, output_path, quality="medium"):
    """
    Compress PDF to reduce file size.
    
    Args:
        input_path: Path to input PDF
        output_path: Path for compressed PDF
        quality: Compression quality (low, medium, high)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        
        quality_settings = {
            "low": 0.3,
            "medium": 0.5,
            "high": 0.75
        }
        
        compression_level = quality_settings.get(quality, 0.5)
        
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        writer.compress_content_streams(level=compression_level)
        
        with open(output_path, "wb") as f:
            writer.write(f)
        
        return True
    except Exception as e:
        print(f"Error compressing PDF: {e}")
        return False


if __name__ == "__main__":
    compress_pdf("large.pdf", "compressed.pdf", "medium")

