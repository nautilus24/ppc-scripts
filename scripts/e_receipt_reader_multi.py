import os
from pdf2image import convert_from_path
import pytesseract
import re
import csv

# Function to process each PDF and extract details
def ocr_receipt(pdf_path):
    # Convert PDF to images
    pages = convert_from_path(pdf_path, 400)  # Increased DPI for better OCR accuracy
    
    # Apply OCR to each page
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page)
    
    return text

# Function to extract relevant details from the OCR text
def extract_details(text):
    lines = text.splitlines()
    
    # Initialize variables
    location = None
    date = None
    total_amount = None
    
    # Extract location: Look for the first line containing an address or store identifier
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

# Function to process all PDFs in a directory
def process_all_pdfs(directory_path):
    all_receipts = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory_path, filename)
            print(f"Processing {pdf_path}")
            ocr_text = ocr_receipt(pdf_path)
            receipt_details = extract_details(ocr_text)
            receipt_details['filename'] = filename
            all_receipts.append(receipt_details)
    
    return all_receipts

# Function to write receipts to a CSV file
def write_receipts_to_csv(receipts, csv_filename):
    # Define the header
    header = ["filename", "location", "date", "total_amount"]
    
    # Write data to CSV file
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for receipt in receipts:
            writer.writerow(receipt)
    
    print(f"Data successfully written to {csv_filename}")

# Directory containing all PDF files
directory_path = "C:/Users/priya/PycharmProjects/PPC/scripts/assets/pdf_assets/e-recipts/"

# Process all PDFs in the directory
all_receipts = process_all_pdfs(directory_path)

# Write the processed data to a CSV file
csv_filename = "receipts_output.csv"
write_receipts_to_csv(all_receipts, csv_filename)

# Print the results
for receipt in all_receipts:
    print(receipt)
