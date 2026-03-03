"""PDF Splitter Module - Split PDF into individual pages"""


def split_pdf(input_file, output_dir):
    """
    Split a PDF into individual pages.
    
    Args:
        input_file: Path to input PDF
        output_dir: Directory to save split pages
    
    Returns:
        list: List of output file paths
    """
    import os
    from PyPDF2 import PdfReader, PdfWriter
    
    try:
        reader = PdfReader(input_file)
        output_files = []
        
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            
            output_path = os.path.join(output_dir, f"page_{i+1}.pdf")
            with open(output_path, "wb") as f:
                writer.write(f)
            
            output_files.append(output_path)
        
        return output_files
    except Exception as e:
        print(f"Error splitting PDF: {e}")
        return []


if __name__ == "__main__":
    split_pdf("input.pdf", "output_pages")

