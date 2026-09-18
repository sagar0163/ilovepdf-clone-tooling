"""PDF Compressor Module - Reduce PDF file size"""

import subprocess
from pathlib import Path

def compress_pdf(input_path, output_path, quality="medium", on_progress=None):
    """
    Compress PDF to reduce file size.
    """
    quality_settings = {
        "low": "/screen",      # lowest quality, smallest file
        "medium": "/ebook",    # medium quality
        "high": "/printer"     # high quality, larger file
    }
    
    gs_quality = quality_settings.get(quality, "/ebook")
    
    input_path = str(Path(input_path).absolute())
    output_path = str(Path(output_path).absolute())
    
    cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={gs_quality}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        # Note: on_progress cannot be accurately reported since gs does not provide page-by-page progress in quiet mode.
        # But we must support the signature.
        if on_progress:
            # We just mock progress at the end if we have no way to poll it,
            # or we could parse gs output if we removed -dQUIET, but a simple 100% is often fine for a subprocess.
            on_progress(1, 1)
        return str(output_path)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Ghostscript compression failed: {e.stderr.decode()}")


if __name__ == "__main__":
    try:
        compress_pdf("large.pdf", "compressed.pdf", "medium")
    except Exception as e:
        print(f"Error compressing PDF: {e}")
