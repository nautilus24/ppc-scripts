import pdfplumber
import pandas as pd
import re
import os

# Set directory containing PDFs
pdf_directory = "scripts/assets/pdf_assets/cc_statement/Chase/2022 ram sapphire/"  # Change this to your actual folder path
output_excel_file = "All_Positive_Transactions.xlsx"
output_text_file = "Extracted_Text.txt"  # Save extracted text for debugging

# Validate directory
if not os.path.exists(pdf_directory):
    print("❌ Error: PDF directory not found!")
    exit()

# List all PDF files in the directory
pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith(".pdf")]

# Initialize a list to store all transactions from all PDFs
all_transactions = []
all_text_data = []  # Store extracted text for debugging

# Regex pattern for valid transactions (ignoring '&' at the start of description)
transaction_pattern = re.compile(r"^(\d{2}/\d{2})\s+&?\s*([\w\s,.*-]+?)\s+(-?\d{1,3}(?:,\d{3})*\.\d{2})$")

# Process each PDF file
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_directory, pdf_file)
    print(f"🔍 Processing: {pdf_file}")

    # Extract text from the PDF
    text_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_data.append(text)
    
    # Save raw extracted text for debugging
    all_text_data.append(f"\n\n--- Extracted from: {pdf_file} ---\n" + "\n".join(text_data))

    # Convert extracted text into a list of lines
    lines = "\n".join(text_data).split("\n")

    # Locate the "PURCHASE" section
    start_index = None
    for i, line in enumerate(lines):
        if "PURCHASE" in line:
            start_index = i + 1  # Start extracting after this line
            break

    # Extract transactions after the section
    transactions = []
    buffer = []  # Temporary storage for multi-line descriptions

    if start_index:
        for line in lines[start_index:]:
            line = line.strip()

            # Skip metadata and headers
            if re.search(r"(Page\s+\d+|Statement Date|ACCOUNT ACTIVITY|CONTINUED|Date of Transaction|Merchant Name|Description \$ Amount)", line, re.IGNORECASE):
                continue

            # Match transaction lines (ignoring '&' at the start of descriptions)
            match = transaction_pattern.match(line)

            if match:
                date = match.group(1)
                description = match.group(2).strip()
                amount = match.group(3).replace(",", "")

                # Merge buffer if it contains previous lines of the same transaction
                if buffer:
                    description = " ".join(buffer + [description])
                    buffer = []

                # Convert to float and add only valid transactions
                transactions.append([pdf_file, date, description, float(amount)])
            else:
                # Store in buffer if it's a multi-line description
                if not re.match(r"^\d{2}/\d{2}", line) and not re.search(r"\d+\.\d{2}$", line):
                    buffer.append(line)
                else:
                    buffer = []  # Reset buffer if line is unclear

    # Append extracted transactions to the main list
    all_transactions.extend(transactions)

# Save extracted text to a file for debugging
with open(output_text_file, "w", encoding="utf-8") as f:
    f.write("\n".join(all_text_data))

# Convert all extracted data into a DataFrame
df_all = pd.DataFrame(all_transactions, columns=["Source File", "Date", "Description", "Amount"])

# Save all transactions to a single Excel file
df_all.to_excel(output_excel_file, index=False)

print(f"✅ All transactions extracted! File saved as: {output_excel_file}")
print(f"📄 Extracted text saved as: {output_text_file}")