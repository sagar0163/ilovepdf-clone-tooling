"""PDF Compressor Module - Reduce PDF file size"""

from core import _copy_pdf

def compress_pdf(input_path, output_path, quality="medium"):
    """
    Compress PDF to reduce file size.
    """
    quality_settings = {
        "low": 0.3,
        "medium": 0.5,
        "high": 0.75
    }
    
    compression_level = quality_settings.get(quality, 0.5)
    def writer_transform(writer):
        writer.compress_content_streams(level=compression_level)

    out = _copy_pdf(input_path, output_path, writer_transform=writer_transform)
    return str(out)

if __name__ == "__main__":
    try:
        compress_pdf("large.pdf", "compressed.pdf", "medium")
    except Exception as e:
        print(f"Error compressing PDF: {e}")
