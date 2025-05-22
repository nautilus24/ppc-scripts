import re
import sys
import pandas as pd
from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    return text

def main():
    pdf_path = 'scripts/assets/PO 330197.pdf'
    text = extract_text_from_pdf(pdf_path)
    print(text)

    # Use regular expressions to find all occurrences of the desired patterns
    # po_numbers = re.findall(r'PO:\s*(\d+)', text)
    quantities = re.findall(r'QTY:\s*(\d+)', text)
    # carton_texts = re.findall(r'Carton \s*([^\n]*)', text)
    store_numbers = re.findall(r'STORE #\s*(\d+)', text)
    # print(store_numbers)
    
    # Combine the extracted values into a list of tuples
    data = list(zip(quantities, store_numbers))
    # print(data)
    
    # Create a pandas dataframe from the data
    df = pd.DataFrame(data, columns=['Quantity','Store Number'])
    print(df)
    
    # Write the dataframe to an Excel file
    df.to_excel('output_temp.xlsx', index=False)
        
if __name__ == '__main__':
    main()
