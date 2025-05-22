import re
from pdf2image import convert_from_path
import pytesseract

# Function to process the PDF and apply OCR
def ocr_statement(pdf_path):
    pages = convert_from_path(pdf_path, 400)
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page)
    return text

# Function to extract withdrawals and debits
def extract_withdrawals(text):
    withdrawals_pattern = re.compile(r"Withdrawals and other debits(?:\s+Date Description Amount\s+)?(.*?)Total withdrawals and other debits", re.DOTALL)
    match = withdrawals_pattern.search(text)
    if match:
        withdrawals_text = match.group(1)
        withdrawals = []
        for line in withdrawals_text.splitlines():
            withdrawal_match = re.search(r"(\d{2}/\d{2}/\d{2})\s+(.+?)\s+\-?\$([\d,]+\.\d{2})", line)
            if withdrawal_match:
                withdrawals.append({
                    "date": withdrawal_match.group(1),
                    "description": withdrawal_match.group(2).strip(),
                    "amount": withdrawal_match.group(3).replace(",", "")
                })
        return withdrawals
    return []

# Function to extract checks
def extract_checks(text):
    checks_pattern = re.compile(r"Checks(?:\s+Date Check # Amount\s+)?(.*?)Total checks", re.DOTALL)
    match = checks_pattern.search(text)
    if match:
        checks_text = match.group(1)
        checks = []
        for line in checks_text.splitlines():
            check_match = re.search(r"(\d{2}/\d{2}/\d{2})\s+(\d+)\s+\-?\$([\d,]+\.\d{2})", line)
            if check_match:
                checks.append({
                    "date": check_match.group(1),
                    "check_number": check_match.group(2),
                    "amount": check_match.group(3).replace(",", "")
                })
        return checks
    return []

# Process the bank statement
pdf_path = "C:/Users/priya/Downloads/eStmt_2018-01-31.pdf"
text = ocr_statement(pdf_path)

# Extract the withdrawals and debits
withdrawals = extract_withdrawals(text)
print("Withdrawals and Debits:")
for withdrawal in withdrawals:
    print(withdrawal)

# Extract the checks
checks = extract_checks(text)
print("\nChecks:")
for check in checks:
    print(check)
