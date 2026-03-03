"""PDF Unlocker Module - Remove password protection from PDF"""


def unlock_pdf(input_path, output_path, password):
    """
    Remove password protection from PDF.
    
    Args:
        input_path: Path to locked PDF
        output_path: Path for unlocked PDF
        password: Password to unlock the PDF
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        
        reader = PdfReader(input_path)
        
        if reader.is_encrypted:
            reader.decrypt(password)
        
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        with open(output_path, "wb") as f:
            writer.write(f)
        
        return True
    except Exception as e:
        print(f"Error unlocking PDF: {e}")
        return False


if __name__ == "__main__":
    unlock_pdf("locked.pdf", "unlocked.pdf", password="secret123")

