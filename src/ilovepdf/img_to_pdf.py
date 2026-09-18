"""Image to PDF Converter - Convert images to PDF document"""


def convert_images_to_pdf(image_paths, output_path, layout="portrait"):
    """
    Convert images to PDF document.
    
    Args:
        image_paths: List of image file paths
        output_path: Path for output PDF
        layout: Page layout (portrait or landscape)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.pdfgen import canvas
        from PIL import Image
        import os
        
        c = canvas.Canvas(output_path, pagesize=A4)
        
        for img_path in image_paths:
            img = Image.open(img_path)
            width, height = img.size
            
            # Calculate aspect ratio
            aspect = height / width
            
            if layout == "landscape":
                c.setPageSize((height, width))
            else:
                c.setPageSize(A4)
            
            c.drawImage(img_path, 0, 0, width=500, height=500*aspect)
            c.showPage()
        
        c.save()
        return True
    except Exception as e:
        print(f"Error converting images to PDF: {e}")
        return False


if __name__ == "__main__":
    convert_images_to_pdf(["photo1.jpg", "photo2.jpg"], "output.pdf")

