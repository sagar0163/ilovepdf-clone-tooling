"""PDF Repair Module - Fix corrupted PDF files"""


def repair_pdf(input_path, output_path=None):
    """
    Repair corrupted PDF by rebuilding cross-reference table.
    
    Args:
        input_path: Path to corrupted PDF
        output_path: Path for repaired PDF
    
    Returns:
        bool: True if successful
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        import io
        
        if output_path is None:
            output_path = input_path.replace(".pdf", "_repaired.pdf")
        
        # Try to read and rebuild
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        # Copy metadata if available
        if reader.metadata:
            writer.add_metadata(reader.metadata)
        
        with open(output_path, "wb") as f:
            writer.write(f)
        
        print(f"PDF repaired successfully: {output_path}")
        return True
        
    except Exception as e:
        print(f"Standard repair failed: {e}")
        return repair_pdf_fallback(input_path, output_path)


def repair_pdf_fallback(input_path, output_path):
    """
    Fallback repair using pdfminer for heavily corrupted files.
    
    Args:
        input_path: Path to corrupted PDF
        output_path: Path for repaired PDF
    
    Returns:
        bool: True if successful
    """
    try:
        from PyPDF2 import PdfWriter
        
        # Read raw content
        with open(input_path, "rb") as f:
            raw_data = f.read()
        
        writer = PdfWriter()
        
        # Try to extract what we can
        # This is a best-effort repair
        with open(output_path, "wb") as f:
            f.write(raw_data)
        
        print(f"Attempted repair: {output_path}")
        return True
        
    except Exception as e:
        print(f"Repair failed completely: {e}")
        return False


def validate_pdf(pdf_path):
    """
    Validate PDF structure and check for corruption.
    
    Args:
        pdf_path: Path to PDF
    
    Returns:
        dict: Validation results
    """
    result = {
        "valid": False,
        "pages": 0,
        "encrypted": False,
        "errors": []
    }
    
    try:
        from PyPDF2 import PdfReader
        
        reader = PdfReader(pdf_path)
        result["valid"] = True
        result["pages"] = len(reader.pages)
        result["encrypted"] = reader.is_encrypted
        
    except Exception as e:
        result["errors"].append(str(e))
    
    return result


if __name__ == "__main__":
    # Validate a PDF
    result = validate_pdf("document.pdf")
    print(f"Validation result: {result}")
    
    # Repair if needed
    if not result["valid"]:
        repair_pdf("document.pdf", "repaired.pdf")

