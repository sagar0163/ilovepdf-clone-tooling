"""PDF Compressor Module - Reduce PDF file size"""

import subprocess
from pathlib import Path

def compress_pdf(input_path, output_path, quality="medium", on_progress=None):
    """
    Compress PDF to reduce file size.
    
    This function uses Ghostscript to perform real image re-encoding, rasterization, 
    and downsampling, which drastically reduces file sizes for image-heavy, 
    scanned, or photographed PDFs. 
    
    For text-only PDFs, the reduction might be minimal compared to raw Flate
    compression, but for image-heavy files, this is the most effective path.
    
    Quality settings map to standard Ghostscript PDFSETTINGS presets:
    - low: /screen (72 dpi, fast, low quality, smallest size)
    - medium: /ebook (150 dpi, medium quality, medium size)
    - high: /printer (300 dpi, high quality, larger size)
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    
    gs_quality_mapping = {
        "low": "/screen",
        "medium": "/ebook",
        "high": "/printer"
    }
    
    pdfsettings = gs_quality_mapping.get(quality, "/ebook")
    
    gs_cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={pdfsettings}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        str(input_path)
    ]
    
    try:
        subprocess.run(gs_cmd, check=True, capture_output=True)
        # We can't granularly track progress per page easily with gs subprocess,
        # so we report 100% completion once the blocking call finishes.
        if on_progress:
            on_progress(1, 1)
        return str(output_path)
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode('utf-8', errors='ignore') if e.stderr else str(e)
        raise Exception(f"Ghostscript compression failed: {error_msg}")

if __name__ == "__main__":
    try:
        compress_pdf("large.pdf", "compressed.pdf", "medium")
    except Exception as e:
        print(f"Error compressing PDF: {e}")
