"""PDF Merger Module - Combine multiple PDF files into one"""


def merge_pdfs(input_files, output_path):
    """
    Merge multiple PDF files into a single PDF.
    
    Args:
        input_files: List of input PDF file paths
        output_path: Path for the output merged PDF
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from PyPDF2 import PdfMerger
        merger = PdfMerger()
        
        for pdf in input_files:
            merger.append(pdf)
        
        merger.write(output_path)
        merger.close()
        
        return True
    except Exception as e:
        print(f"Error merging PDFs: {e}")
        return False


if __name__ == "__main__":
    # Example usage
    files = ["file1.pdf", "file2.pdf"]
    merge_pdfs(files, "merged.pdf")

