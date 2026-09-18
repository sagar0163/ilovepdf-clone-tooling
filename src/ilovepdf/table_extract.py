"""Table Extraction - Convert PDF tables to CSV/Excel"""


def extract_tables(pdf_path, output_format="csv"):
    """
    Extract tables from PDF and convert to CSV or Excel.
    
    Args:
        pdf_path: Path to input PDF
        output_format: Output format (csv or xlsx)
    
    Returns:
        list: List of output file paths
    """
    try:
        from PyPDF2 import PdfReader
        import csv
        import pandas as pd
        
        reader = PdfReader(pdf_path)
        output_files = []
        
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            
            # Simple table detection (lines with consistent delimiters)
            lines = text.split("\n")
            table_data = []
            
            for line in lines:
                # Detect table-like lines (with tabs or multiple spaces)
                if "\t" in line or "  " in line:
                    cells = line.replace("\t", ",").split(",")
                    table_data.append([c.strip() for c in cells])
            
            if table_data:
                output_path = f"table_page_{page_num + 1}.{output_format}"
                
                if output_format == "csv":
                    with open(output_path, "w", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerows(table_data)
                else:
                    df = pd.DataFrame(table_data[1:], columns=table_data[0])
                    df.to_excel(output_path, index=False)
                
                output_files.append(output_path)
        
        return output_files
    except Exception as e:
        print(f"Error extracting tables: {e}")
        return []


def extract_table_from_page(pdf_path, page_number=0):
    """
    Extract table from a specific page.
    
    Args:
        pdf_path: Path to PDF
        page_number: Page number (0-indexed)
    
    Returns:
        list: Table data as list of lists
    """
    try:
        from PyPDF2 import PdfReader
        
        reader = PdfReader(pdf_path)
        page = reader.pages[page_number]
        text = page.extract_text()
        
        lines = text.split("\n")
        table_data = []
        
        for line in lines:
            if "  " in line or "\t" in line:
                cells = line.replace("\t", ",").split(",")
                table_data.append([c.strip() for c in cells])
        
        return table_data
    except Exception as e:
        print(f"Error extracting table: {e}")
        return []


if __name__ == "__main__":
    files = extract_tables("document.pdf", output_format="csv")
    print(f"Extracted {len(files)} tables")

