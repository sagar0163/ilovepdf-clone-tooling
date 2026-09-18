"""Progress Bar Support - Add tqdm progress bars for CLI"""
from tqdm import tqdm
from ilovepdf.merge import merge_pdfs
from ilovepdf.split import split_pdf
from ilovepdf.compress import compress_pdf

def merge_with_progress(input_files, output_path, show_progress=True):
    if not show_progress:
        return merge_pdfs(input_files, output_path)
        
    pbar = tqdm(total=len(input_files), desc="Merging PDFs", unit="file")
    def on_progress(i, total):
        pbar.update(1)
        
    try:
        res = merge_pdfs(input_files, output_path, on_progress=on_progress)
        pbar.close()
        return bool(res)
    except Exception as e:
        pbar.close()
        print(f"Error merging: {e}")
        return False


def split_with_progress(input_file, output_dir, show_progress=True):
    if not show_progress:
        try:
            return split_pdf(input_file, output_dir)
        except:
            return []
            
    pbar = None
    def on_progress(i, total):
        nonlocal pbar
        if pbar is None:
            pbar = tqdm(total=total, desc="Splitting pages", unit="page")
        pbar.update(1)
        
    try:
        res = split_pdf(input_file, output_dir, on_progress=on_progress)
        if pbar: pbar.close()
        return res
    except Exception as e:
        if pbar: pbar.close()
        print(f"Error splitting: {e}")
        return []


def compress_with_progress(input_path, output_path, quality="medium", show_progress=True):
    if not show_progress:
        try:
            return bool(compress_pdf(input_path, output_path, quality=quality))
        except:
            return False
            
    pbar = None
    def on_progress(i, total):
        nonlocal pbar
        if pbar is None:
            pbar = tqdm(total=total, desc="Compressing", unit="page")
        pbar.update(1)
        
    try:
        res = compress_pdf(input_path, output_path, quality=quality, on_progress=on_progress)
        if pbar: pbar.close()
        return bool(res)
    except Exception as e:
        if pbar: pbar.close()
        print(f"Error compressing: {e}")
        return False


if __name__ == "__main__":
    print("Testing merge with progress...")
    merge_with_progress(["file1.pdf", "file2.pdf"], "merged.pdf")
