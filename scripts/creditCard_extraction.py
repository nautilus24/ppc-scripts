import pdfplumber

pdf_path = "scripts/assets/pdf_assets/cc_statement/test.pdf"  # Replace with actual file path

# Step 1: Extract and print text from the PDF
with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages):
        text = page.extract_text()
        print(f"--- Page {page_num + 1} ---\n")
        print(text)
        print("\n" + "=" * 80 + "\n")

# Step 2: Locate "Total New Charges" in the text
text_data = []
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text_data.extend(page.extract_text().split("\n"))

for i, line in enumerate(text_data):
    if "Total New Charges" in line:
        print(f"'Total New Charges' found on line {i}: {line}")

# Step 3: Print transactions after "Total New Charges"
start_index = None
for i, line in enumerate(text_data):
    if "Total New Charges" in line:
        start_index = i + 1
        break

if start_index:
    print("\nExtracted Transactions After 'Total New Charges':\n")
    for line in text_data[start_index : start_index + 10]:  # Print first 10 lines after it
        print(line)
else:
    print("No 'Total New Charges' found in the text.")



import pdfplumber
import pandas as pd

# Path to your PDF file
pdf_path = "scripts/assets/pdf_assets/cc_statement/test.pdf"  # Replace with the actual path to your file

# Extract text from the PDF
text_data = []
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text_data.extend(page.extract_text().split("\n"))

# Locate "Total New Charges" and extract transactions after it
start_index = None
for i, line in enumerate(text_data):
    if "Total New Charges" in line:
        start_index = i + 1  # Transactions start right after this
        break

# Extract transactions from the structured format
transactions = []
if start_index:
    i = start_index
    while i < len(text_data) - 2:
        try:
            # Ensure we have three consecutive lines forming a transaction
            date = text_data[i].strip()
            description = text_data[i + 1].strip()
            amount = text_data[i + 2].strip()

            # Validate amount format (should start with "$")
            if amount.startswith("$"):
                amount = amount.replace("$", "").replace(",", "")
                transactions.append([date, description, float(amount)])
                i += 3  # Move to the next transaction
            else:
                i += 1  # Skip invalid row

        except IndexError:
            break

# Convert to DataFrame
df_payments = pd.DataFrame(transactions, columns=["Date", "Description", "Amount"])

# Save as Excel file
excel_path = "New_Payments.xlsx"  # Save the output file in the same directory
df_payments.to_excel(excel_path, index=False)

print(f"✅ Extraction Complete! File saved as: {excel_path}")
