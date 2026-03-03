"""Progress Bar Support - Add tqdm progress bars for CLI"""


def merge_with_progress(input_files, output_path, show_progress=True):
    """
    Merge PDFs with progress bar.
    
    Args:
        input_files: List of input PDF paths
        output_path: Output file path
        show_progress: Show progress bar
    
    Returns:
        bool: True if successful
    """
    try:
        from PyPDF2 import PdfMerger
        from tqdm import tqdm
        
        merger = PdfMerger()
        
        if show_progress:
            iterator = tqdm(input_files, desc="Merging PDFs", unit="file")
        else:
            iterator = input_files
        
        for pdf in iterator:
            merger.append(pdf)
        
        merger.write(output_path)
        merger.close()
        
        return True
    except Exception as e:
        print(f"Error merging: {e}")
        return False


def split_with_progress(input_file, output_dir, show_progress=True):
    """
    Split PDF with progress bar.
    
    Args:
        input_file: Input PDF path
        output_dir: Output directory
        show_progress: Show progress bar
    
    Returns:
        list: List of output files
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        import os
        from tqdm import tqdm
        
        reader = PdfReader(input_file)
        total_pages = len(reader.pages)
        
        if show_progress:
            pbar = tqdm(total=total_pages, desc="Splitting pages", unit="page")
        
        output_files = []
        
        for i in range(total_pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])
            
            output_path = os.path.join(output_dir, f"page_{i+1}.pdf")
            with open(output_path, "wb") as f:
                writer.write(f)
            
            output_files.append(output_path)
            
            if show_progress:
                pbar.update(1)
        
        if show_progress:
            pbar.close()
        
        return output_files
    except Exception as e:
        print(f"Error splitting: {e}")
        return []


def compress_with_progress(input_path, output_path, quality="medium", show_progress=True):
    """
    Compress PDF with progress indication.
    
    Args:
        input_path: Input PDF path
        output_path: Output file path
        quality: Compression quality
        show_progress: Show progress bar
    
    Returns:
        bool: True if successful
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        from tqdm import tqdm
        
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        
        writer = PdfWriter()
        
        if show_progress:
            iterator = tqdm(reader.pages, desc="Compressing", unit="page")
        else:
            iterator = reader.pages
        
        for page in iterator:
            writer.add_page(page)
        
        writer.compress_content_streams()
        
        with open(output_path, "wb") as f:
            writer.write(f)
        
        return True
    except Exception as e:
        print(f"Error compressing: {e}")
        return False


if __name__ == "__main__":
    # Test with progress bars
    print("Testing merge with progress...")
    merge_with_progress(["file1.pdf", "file2.pdf"], "merged.pdf")

