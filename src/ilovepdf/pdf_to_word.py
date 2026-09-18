"""PDF to Word Converter - Convert PDF documents to Word format"""


def convert_to_word(pdf_path, output_path=None):
    """
    Convert PDF to Word document (.docx).
    
    Args:
        pdf_path: Path to input PDF
        output_path: Path for output DOCX file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from pdf2docx import Converter
        
        if output_path is None:
            output_path = pdf_path.replace(".pdf", ".docx")
        
        cv = Converter(pdf_path)
        cv.convert(output_path)
        cv.close()
        
        return True
    except Exception as e:
        print(f"Error converting PDF to Word: {e}")
        return False


if __name__ == "__main__":
    convert_to_word("document.pdf", "document.docx")

