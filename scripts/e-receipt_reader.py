import re
from pdf2image import convert_from_path
import pytesseract

# Step 1: Convert PDF to images and apply OCR
def ocr_receipt(pdf_path):
    # Convert PDF to images
    pages = convert_from_path(pdf_path, 400)
    
    # Apply OCR to each page
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page)
    
    return text

# Step 2: Extract relevant details from the OCR text
def extract_details(text):
    lines = text.splitlines()
    
    # Initialize variables
    location = None
    date = None
    total_amount = None
    
    # Extract location: Look for a line that contains common address patterns
    for i, line in enumerate(lines):
        if re.search(r'\d{1,5}\s+\w+\s+(BLVD|ST|AVE|ROAD|RD|DR|HWY|HIGHWAY)', line.upper()):
            location = line.strip()
            # Optionally, check subsequent lines to capture city/state if it's on the next line
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if re.search(r'\w+,\s*[A-Z]{2}', next_line):  # Check for City, State format
                    location += ", " + next_line
            break
    
    # Extract date
    date_pattern = re.compile(r'\d{2}/\d{2}/\d{2}')
    for line in lines:
        match = date_pattern.search(line)
        if match:
            date = match.group()
            break
    
    # Extract total amount: Look for the line containing "TOTAL"
    for line in lines:
        if "TOTAL" in line.upper():
            amount_match = re.search(r'-?\$\d+[\.,]\d{2}', line)
            if amount_match:
                total_amount = amount_match.group().replace('$', '').replace(',', '')
                break
    
    return {
        "location": location,
        "date": date,
        "total_amount": total_amount
    }

# Example Usage
pdf_path = "C:/Users/priya/PycharmProjects/PPC/scripts/assets/pdf_assets/e-recipts/eReceipt(55).pdf"
ocr_text = ocr_receipt(pdf_path)
receipt_details = extract_details(ocr_text)

# Display the extracted details
print("Extracted Details:\n", receipt_details)
