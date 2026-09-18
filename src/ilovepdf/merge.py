"""PDF Merger Module - Combine multiple PDF files into one"""

def merge_pdfs(input_files, output_path, on_progress=None):
    """
    Merge multiple PDF files into a single PDF.
    """
    from PyPDF2 import PdfMerger
    merger = PdfMerger()
    
    total = len(input_files)
    for i, pdf in enumerate(input_files):
        merger.append(pdf)
        if on_progress:
            on_progress(i, total)
    
    merger.write(output_path)
    merger.close()
    
    return str(output_path)

if __name__ == "__main__":
    try:
        merge_pdfs(["file1.pdf", "file2.pdf"], "merged.pdf")
    except Exception as e:
        print(f"Error merging PDFs: {e}")
