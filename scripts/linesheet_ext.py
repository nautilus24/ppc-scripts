import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import pandas as pd

# Specify the path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'  # Update this with your Tesseract path

# Convert PDF to images
pages = convert_from_path('scripts/assets/Linesheet Extractor/GIRLS BTS 2024 LINESHEET.pdf', 300)  # Update this with your PDF path

# Initialize a list to hold all products
products = []

# Use OCR to extract text from each image
for i, page in enumerate(pages):
    text = pytesseract.image_to_string(page, lang='eng')
    lines = text.split('\n')
    
    # Temporary dictionary to hold the current product's information
    product = {}
    
    for line in lines:
        if 'Name:' in line:
            product['Name'] = line.split(': ')[1]
        elif 'Description:' in line:
            product['Description'] = line.split(': ')[1]
        elif 'Style#:' in line:
            product['Style#'] = line.split(': ')[1]
        elif 'Color:' in line:
            product['Color'] = line.split(': ')[1]
        elif 'Price:' in line:
            product['Price'] = line.split(': ')[1]
    
    # If a product dictionary has been filled, add it to the products list
    if product:
        products.append(product)

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(products)
# Save the DataFrame to an Excel file
print(df.head())
# df.to_excel('/path/to/save/your_excel_file.xlsx', index=False)