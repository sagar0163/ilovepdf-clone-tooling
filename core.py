"""Core PDF utilities and shared operations."""

from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter

def _copy_pdf(input_path, output_path, password=None, page_transform=None, writer_transform=None):
    """
    Core function to copy a PDF and apply transformations.
    
    Args:
        input_path: Path to input PDF.
        output_path: Path to output PDF.
        password: Password to decrypt the input PDF, if required.
        page_transform: Function(page_num, page) -> None. Called for each page before adding.
        writer_transform: Function(writer) -> None. Called on writer before saving.
        
    Returns:
        Path: Path to the output file.
        
    Raises:
        Exception: Propagates any PyPDF2 exceptions or I/O errors.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    
    reader = PdfReader(input_path)
    if password is not None:
        if not reader.decrypt(password):
            raise ValueError("Incorrect password")
            
    writer = PdfWriter()
    
    for i, page in enumerate(reader.pages):
        if page_transform:
            page_transform(i, page)
        writer.add_page(page)
        
    if writer_transform:
        writer_transform(writer)
        
    with open(output_path, "wb") as f:
        writer.write(f)
        
    return output_path


def _split_pdf(input_path, output_dir):
    """
    Core function to split a PDF into individual pages.
    
    Args:
        input_path: Path to input PDF.
        output_dir: Directory to save split pages.
        
    Returns:
        list of Path: List of output file paths.
    """
    from PyPDF2 import PdfReader, PdfWriter
    
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    reader = PdfReader(input_path)
    output_files = []
    
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        
        out_path = output_dir / f"page_{i+1}.pdf"
        with open(out_path, "wb") as f:
            writer.write(f)
        output_files.append(out_path)
        
    return output_files
