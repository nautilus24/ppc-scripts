# import re  
# import pandas as pd

# from pdfminer.high_level import extract_text

# def extract_text_from_pdf(pdf_path):
#     text = extract_text(pdf_path)
#     return text

# if __name__ == "__main__":
#     path_to_pdf = 'scripts/assets/pdf_assets/a997vonmaur40214092744.pdf'  # Replace with your PDF file path
#     extracted_text = extract_text_from_pdf(path_to_pdf)
    
#     # Regular expression patterns to match the store number and total, considering the structure mentioned
#     store_no_pattern = r"STORE NO:\s*\n\s*\n(\d+)"
#     total_pattern = r"TOTAL\s*\n\s*\n\$(\d+,\d+\.\d{2})"  # Assuming the total format is "$<amount>"
    
#     # Finding all matches in the extracted text
#     store_numbers = re.findall(store_no_pattern, extracted_text)
#     totals = re.findall(total_pattern, extracted_text)
    
#     # Creating a DataFrame from the extracted values
#     df = pd.DataFrame({
#         "Store No": store_numbers,
#         "Total": totals
#     })
    
#     # Display the DataFrame
#     print(df)
    
#     # Optional: Save the DataFrame to an Excel file
#     # df.to_excel('output_store_totals.xlsx', index=False)

# import re
# import pandas as pd
# from pdfminer.high_level import extract_text

# def extract_text_from_pdf(pdf_path):
#     text = extract_text(pdf_path)
#     return text

# if __name__ == "__main__":
#     path_to_pdf = 'scripts/assets/pdf_assets/a997vonmaur40214092744.pdf'  # Replace with your PDF file path
#     extracted_text = extract_text_from_pdf(path_to_pdf)
    
#     # Regular expression patterns to match the store number and total
#     store_no_pattern = r"STORE NO:\s*\n\s*\n(\d+)"
#     total_pattern = r"TOTAL\s*\n\s*\n\$(\d+,\d+\.\d{2})"  # Adjusted for format
    
#     # Finding all matches in the extracted text
#     store_numbers = re.findall(store_no_pattern, extracted_text)
#     totals = re.findall(total_pattern, extracted_text)
#     # print(len(store_numbers))
#     # print(len(totals))
#     print(store_numbers)
#     # Check if lists have the same length
#     if len(store_numbers) == len(totals):
#         # Creating a DataFrame from the extracted values
#         df = pd.DataFrame({
#             "Store No": store_numbers,
#             "Total": totals
#         })
        
#         # Display the DataFrame
#         print(df)
        
#         # Optional: Save the DataFrame to an Excel file
#         df.to_excel('output_store_totals.xlsx', index=False)
#     else:
#         print("Mismatch in the number of store numbers and totals found. Please check the extracted data.")


import re  
import pandas as pd
from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    return text

def extract_store_no_and_total(text):
    # Split the text into lines
    lines = text.split('\n')
    
    store_numbers = []
    totals = []
    
    for i, line in enumerate(lines):
        if "STORE NO:" in line:
            # Assuming the store number is two lines down from "STORE NO:"
            if i+3 < len(lines):  # Ensure we don't go out of index
                store_numbers.append(lines[i+2].strip())
                
        if "TOTAL" in line:
            # Assuming the total is two lines down from "TOTAL"
            if i+3 < len(lines):  # Ensure we don't go out of index
                totals.append(lines[i+2].strip())
                
    return store_numbers, totals

if __name__ == "__main__":
    path_to_pdf = 'scripts/assets/pdf_assets/a997vonmaur40214092744.pdf'  # Adjust the path to your PDF file
    extracted_text = extract_text_from_pdf(path_to_pdf)
    
    store_numbers, totals = extract_store_no_and_total(extracted_text)
    
    # Creating a DataFrame from the extracted values
    # Ensure both lists have the same length
    if len(store_numbers) == len(totals):
        df = pd.DataFrame({
            "Store No": store_numbers,
            "Total": totals
        })
    else:
        # Handling the case where the lengths do not match
        # This is a simple fix; for a real scenario, you'd need to ensure the data aligns correctly
        min_length = min(len(store_numbers), len(totals))
        df = pd.DataFrame({
            "Store No": store_numbers[:min_length],
            "Total": totals[:min_length]
        })
    
    print(df)
