import os
import glob
import re
import pdfplumber
import pandas as pd

# Folder containing PDF statements
pdf_folder = "scripts/assets/pdf_assets/bofa statements/SAM 2023/"
output_txt_folder = "extracted_txt_files/BOFA/SAM 2023/"
os.makedirs(output_txt_folder, exist_ok=True)

# To hold all parsed transactions
all_transactions = []

def extract_withdrawals_from_pdf(pdf_path, output_txt_path):
    withdrawals_text = []
    start_extracting = False

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if "Withdrawals and other debits" in text:
                start_extracting = True
            if start_extracting:
                withdrawals_text.append(text)

    all_text = "\n".join(withdrawals_text)
    start_index = all_text.find("Withdrawals and other debits")
    extracted_text = all_text[start_index:]

    with open(output_txt_path, "w") as file:
        file.write(extracted_text)

def parse_withdrawals_from_txt(txt_path):
    with open(txt_path, "r") as file:
        text = file.read()

    pattern = re.compile(r"(\d{2}/\d{2}/\d{2})\s+(.+?)\s+(-\d{1,3}(?:,\d{3})*(?:\.\d{2}))")
    matches = pattern.findall(text)
    
    transactions = []
    for match in matches:
        date = match[0]
        description = match[1].strip()
        amount = float(match[2].replace(",", ""))
        transactions.append([date, description, amount])

    return transactions

# Main loop: process all PDFs
for pdf_file in glob.glob(os.path.join(pdf_folder, "*.pdf")):
    filename = os.path.splitext(os.path.basename(pdf_file))[0]
    txt_path = os.path.join(output_txt_folder, f"{filename}.txt")
    extract_withdrawals_from_pdf(pdf_file, txt_path)
    transactions = parse_withdrawals_from_txt(txt_path)
    all_transactions.extend(transactions)

# Save all collected transactions to Excel
df_all = pd.DataFrame(all_transactions, columns=["Date", "Description", "Amount"])
print(df_all)
df_all.to_excel("combined_withdrawals.xlsx", index=False)
print("✅ Combined Excel file created: combined_withdrawals.xlsx")
