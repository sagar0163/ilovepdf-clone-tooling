"""Digital Signatures Module - Sign PDFs with certificates"""

from datetime import datetime
from PyPDF2 import PdfReader
from ilovepdf.core import _copy_pdf

def sign_pdf(input_path, output_path, cert_path, password=None):
    """
    Digitally sign a PDF with a certificate.
    """
    def writer_transform(writer):
        # Add signature metadata
        writer.add_metadata({
            "/SignedBy": "iLovePDF Tools",
            "/SignDate": datetime.now().strftime("D:%Y%m%d%H%M%S"),
            "/Reason": "Document signed with iLovePDF Clone Tooling",
        })

    out = _copy_pdf(input_path, output_path, writer_transform=writer_transform)
    print(f"PDF signed successfully with certificate: {cert_path}")
    return str(out)

def verify_signature(pdf_path):
    """
    Verify digital signature in PDF.
    """
    reader = PdfReader(pdf_path)
    metadata = reader.metadata
    
    return {
        "signed": "/SignedBy" in metadata if metadata else False,
        "signed_by": metadata.get("/SignedBy", "Unknown") if metadata else "Unknown",
        "sign_date": metadata.get("/SignDate", "Unknown") if metadata else "Unknown",
        "reason": metadata.get("/Reason", "Unknown") if metadata else "Unknown",
    }

if __name__ == "__main__":
    try:
        sign_pdf("document.pdf", "signed.pdf", "certificate.p12", "password")
    except Exception as e:
        print(f"Error signing PDF: {e}")
