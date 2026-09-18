"""PDF Protection Module - Encrypt and protect PDF files"""

from ilovepdf.core import _copy_pdf

def encrypt_pdf(input_path, output_path, password, owner_password=None):
    """
    Add password protection/encryption to PDF.
    """
    if owner_password is None:
        owner_password = password
        
    def writer_transform(writer):
        writer.encrypt(user_password=password, owner_password=owner_password)
        
    out = _copy_pdf(input_path, output_path, writer_transform=writer_transform)
    return str(out)

if __name__ == "__main__":
    try:
        encrypt_pdf("document.pdf", "protected.pdf", password="secret123")
    except Exception as e:
        print(f"Error encrypting PDF: {e}")
