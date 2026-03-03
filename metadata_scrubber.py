"""Metadata Scrubber - Remove hidden metadata from PDFs for privacy"""


def scrub_metadata(input_path, output_path, keep_creator=False):
    """
    Remove hidden metadata from PDF for privacy.
    
    Args:
        input_path: Path to input PDF
        output_path: Path for cleaned PDF
        keep_creator: Keep creator info (default: False)
    
    Returns:
        bool: True if successful
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        # Remove all metadata
        writer.add_metadata({})
        
        # Or keep minimal metadata
        if keep_creator:
            writer.add_metadata({
                "/Creator": "iLovePDF Tools",
            })
        
        with open(output_path, "wb") as f:
            writer.write(f)
        
        return True
    except Exception as e:
        print(f"Error scrubbing metadata: {e}")
        return False


def get_metadata(pdf_path):
    """
    Extract all metadata from PDF.
    
    Args:
        pdf_path: Path to PDF
    
    Returns:
        dict: Metadata key-value pairs
    """
    try:
        from PyPDF2 import PdfReader
        
        reader = PdfReader(pdf_path)
        metadata = reader.metadata
        
        if metadata:
            return {k.strip("/"): v for k, v in metadata.items()}
        return {}
    except Exception as e:
        print(f"Error getting metadata: {e}")
        return {}


if __name__ == "__main__":
    # Extract metadata first
    meta = get_metadata("document.pdf")
    print("Current metadata:", meta)
    
    # Scrub metadata
    scrub_metadata("document.pdf", "cleaned.pdf")

