"""Metadata Scrubber - Remove hidden metadata from PDFs for privacy"""

from ilovepdf.core import _copy_pdf

def scrub_metadata(input_path, output_path, keep_creator=False):
    """
    Remove hidden metadata from PDF for privacy.
    """
    def writer_transform(writer):
        writer.add_metadata({})
        if keep_creator:
            writer.add_metadata({"/Creator": "iLovePDF Tools"})

    out = _copy_pdf(input_path, output_path, writer_transform=writer_transform)
    return str(out)

def get_metadata(pdf_path):
    """
    Extract all metadata from PDF.
    """
    from PyPDF2 import PdfReader
    
    reader = PdfReader(pdf_path)
    metadata = reader.metadata
    
    if metadata:
        return {k.strip("/"): v for k, v in metadata.items()}
    return {}

if __name__ == "__main__":
    try:
        # Extract metadata first
        meta = get_metadata("document.pdf")
        print("Current metadata:", meta)
        
        # Scrub metadata
        scrub_metadata("document.pdf", "cleaned.pdf")
    except Exception as e:
        print(f"Error scrubbing metadata: {e}")
