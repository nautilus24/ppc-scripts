import pdfplumber
import pandas as pd
import re

# Define input and output files
pdf_path = "scripts/assets/pdf_assets/PRECISION APPAREL CUSTOMER REPORT 031825.pdf"  # Change to actual file path
output_excel_file = "QuickBooks_Report.xlsx"

# List to store extracted transaction data
transactions = []

# Regular expression to match transaction lines
# Regular expression to match transaction lines
transaction_pattern = re.compile(r"(Invoice|Payment|Credit Memo)\s+(\d{2}/\d{2}/\d{4})\s+([\w\d-]+)\s+(.+?)\s+Accounts Receivable\s+(.+?)\s+([\d,.-]+)")

# Extract text from the PDF
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            lines = text.split("\n")
            for line in lines:
                match = transaction_pattern.search(line)
                if match:
                    trans_type = match.group(1)
                    date = match.group(2)
                    num = match.group(3)
                    memo = match.group(4).strip()
                    split = match.group(5).strip()
                    amount = match.group(6).replace(",", "").strip()  # Remove commas for numerical consistency

                    # Handle missing or invalid amounts
                    try:
                        amount = float(amount) if amount not in ["-", ""] else 0.0
                    except ValueError:
                        print(f"Skipping invalid amount: {amount} in line: {line}")
                        continue

                    transactions.append([trans_type, date, num, memo, split, amount])

# Convert the extracted data into a DataFrame
df = pd.DataFrame(transactions, columns=["Type", "Date", "Number", "Memo", "Split", "Amount"])

# Save to Excel
df.to_excel(output_excel_file, index=False)

print(f"✅ Extraction complete! File saved as: {output_excel_file}")