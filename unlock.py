"""PDF Unlocker Module - Remove password protection from PDF"""

from core import _copy_pdf

def unlock_pdf(input_path, output_path, password):
    """
    Remove password protection from PDF.
    """
    out = _copy_pdf(input_path, output_path, password=password)
    return str(out)

if __name__ == "__main__":
    try:
        unlock_pdf("locked.pdf", "unlocked.pdf", password="secret123")
    except Exception as e:
        print(f"Error unlocking PDF: {e}")
