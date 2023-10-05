import re
import sys
import pandas as pd
from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    return text

def main():
    pdf_path = 'scripts/assets/data_pdf_2.pdf'
    text = extract_text_from_pdf(pdf_path)
    #print(text)

    # Use regular expressions to find all occurrences of the desired patterns
    po_numbers = re.findall(r'PO:\s*(\d+)', text)
    quantities = re.findall(r'CASE QTY:\s*(\d+)', text)
    carton_texts = re.findall(r'Carton\s*([^\n]*)', text)
    store_numbers = re.findall(r'STORE #\s*(\d+)', text)
    
    # Combine the extracted values into a list of tuples
    data = list(zip(po_numbers, quantities, carton_texts, store_numbers))
    
    # Create a pandas dataframe from the data
    df = pd.DataFrame(data, columns=['PO Number', 'Quantity', 'Carton', 'Store Number'])
    
    # Write the dataframe to an Excel file
    df.to_excel('output.xlsx', index=False)
        
if __name__ == '__main__':
    main()
