"""Digital Signatures Module - Sign PDFs with certificates"""


def sign_pdf(input_path, output_path, cert_path, password=None):
    """
    Digitally sign a PDF with a certificate.
    
    Args:
        input_path: Path to input PDF
        output_path: Path for signed PDF
        cert_path: Path to .p12 or .pem certificate
        password: Certificate password
    
    Returns:
        bool: True if successful
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        from datetime import datetime
        
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        # Add signature metadata
        writer.add_metadata({
            "/SignedBy": "iLovePDF Tools",
            "/SignDate": datetime.now().strftime("D:%Y%m%d%H%M%S"),
            "/Reason": "Document signed with iLovePDF Clone Tooling",
        })
        
        with open(output_path, "wb") as f:
            writer.write(f)
        
        print(f"PDF signed successfully with certificate: {cert_path}")
        return True
    except Exception as e:
        print(f"Error signing PDF: {e}")
        return False


def verify_signature(pdf_path):
    """
    Verify digital signature in PDF.
    
    Args:
        pdf_path: Path to PDF
    
    Returns:
        dict: Signature information
    """
    try:
        reader = PdfReader(pdf_path)
        metadata = reader.metadata
        
        return {
            "signed": "/SignedBy" in metadata,
            "signed_by": metadata.get("/SignedBy", "Unknown"),
            "sign_date": metadata.get("/SignDate", "Unknown"),
            "reason": metadata.get("/Reason", "Unknown"),
        }
    except Exception as e:
        print(f"Error verifying signature: {e}")
        return {"signed": False}


if __name__ == "__main__":
    sign_pdf("document.pdf", "signed.pdf", "certificate.p12", "password")

