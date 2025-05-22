import re
import pandas as pd
from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    return text

def extract_information(text):
    # Use regex to capture all the required information
    pattern = re.compile(
        r"DC #(?P<dc>\d{4})\s+.*?Carton (?P<carton>\d+ of \d+)\s+.*?CASE QTY: (?P<case_qty>\d+)",
        re.DOTALL
    )
    
    matches = pattern.finditer(text)
    
    data = []
    for match in matches:
        dc = match.group('dc')
        carton = match.group('carton')
        case_qty = match.group('case_qty')
        data.append([dc, carton, case_qty])
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=["DC#", "Carton", "Case QTY"])
    
    return df

if __name__ == "__main__":
    path_to_pdf = 'scripts/assets/pdf_assets/LM41021150555_FIXF5E77_LBL_230NORDSTRO.pdf'  # Corrected path
    extracted_text = extract_text_from_pdf(path_to_pdf)
    df = extract_information(extracted_text)
    print(df)
    
    # Save DataFrame to an Excel file
    output_path = 'extracted_data.xlsx'
    df.to_excel(output_path, index=False)
    print(f"Data saved to {output_path}")
