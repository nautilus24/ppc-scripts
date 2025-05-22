import re
import pandas as pd
from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    return text

def extract_store_numbers(text):
    # Regex pattern to capture only the store number after "STORE #"
    pattern = re.compile(r"STORE\s+#\s*(\d+)", re.IGNORECASE)
    
    # Find all matches for store numbers
    store_numbers = pattern.findall(text)
    
    # Create DataFrame with store numbers in a single column
    df = pd.DataFrame(store_numbers, columns=["Store#"])
    
    return df

if __name__ == "__main__":
    path_to_pdf = 'scripts/assets/pdf_assets/LM41021150555_FIXF5E77_LBL_230NORDSTRO.pdf'  # Correct path
    extracted_text = extract_text_from_pdf(path_to_pdf)
    df = extract_store_numbers(extracted_text)
    print(df)
    
    # Save DataFrame to an Excel file
    output_path = 'store_numbers_only.xlsx'
    df.to_excel(output_path, index=False)
    print(f"Data saved to {output_path}")
