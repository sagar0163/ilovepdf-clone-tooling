"""PDF Protection Module - Encrypt and protect PDF files"""


def encrypt_pdf(input_path, output_path, password, owner_password=None):
    """
    Add password protection/encryption to PDF.
    
    Args:
        input_path: Path to input PDF
        output_path: Path for encrypted PDF
        password: User password (for opening)
        owner_password: Owner password (for full permissions)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        
        if owner_password is None:
            owner_password = password
        
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        writer.encrypt(user_password=password, owner_password=owner_password)
        
        with open(output_path, "wb") as f:
            writer.write(f)
        
        return True
    except Exception as e:
        print(f"Error encrypting PDF: {e}")
        return False


if __name__ == "__main__":
    encrypt_pdf("document.pdf", "protected.pdf", password="secret123")

