import pandas as pd
from PyPDF2 import PdfReader
import re

# Open the PDF file
pdf_path = "scripts/assets/Linesheet Extractor/GIRLS BTS 2024 LINESHEET.pdf"
pdf_reader = PdfReader(pdf_path)

# Extract text from each page
pdf_text = ""
for page in pdf_reader.pages:
    pdf_text += page.extract_text() + "\n"

# Print the extracted text to verify
print(pdf_text[:10000])  # Print more text to understand the structure

# Define regex patterns to extract product details
product_pattern = re.compile(r"""
    (?P<name>^[A-Z\s\-]+(?:[A-Z\s\-]+)?)\n
    (?:CREW TEE|DISTRESSED CROP TOP|PULLOVER|CROP PULLOVER)\s*\|\s*[^\n]*\n
    (?P<code>PPC-\w+)\s*\|\s*(?P<color>\w+)\s*\|\s*\$\d+
    """, re.VERBOSE | re.MULTILINE)

# Lists to store extracted data
products = []

# Find all matches for product details
matches = product_pattern.finditer(pdf_text)
for match in matches:
    name = match.group("name").strip()
    code = match.group("code").strip()
    color = match.group("color").strip()

    # Append to list
    products.append([name, code, color])

# Create DataFrame
df = pd.DataFrame(products, columns=["Name", "Style Number", "Color"])

# Print the DataFrame to verify contents
print(df)

# Save to Excel
# excel_path = "scripts/assets/Linesheet Extractor/product_details.xlsx"
# df.to_excel(excel_path, index=False)

# # Provide download link
# import shutil
# shutil.move(excel_path, "scripts/assets/Linesheet Extractor/GIRLS_BTS_2024_Linesheet_Products.xlsx")
