import pandas as pd
import re
import os

# Folder containing extracted text files
input_folder = "extracted_txt_files/2022 ram delta/"  # Adjust this path
output_excel_file = "Formatted_Transactions.xlsx"

# List all text files in the folder
txt_files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]

# Initialize a list to store all transactions from multiple files
all_transactions = []

# Regular expression to detect a transaction entry (Date + Description + Amount)
transaction_pattern = re.compile(r"(\d{2}/\d{2}/\d{2})\s+(.+?)\s+\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)")

for txt_file in txt_files:
    input_text_file = os.path.join(input_folder, txt_file)

    # Read the text file
    with open(input_text_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Extract transactions from each file
    for line in lines:
        match = transaction_pattern.search(line)
        if match:
            date = match.group(1)
            description = match.group(2).strip()
            amount = match.group(3).replace(",", "")  # Remove commas for numerical consistency
            all_transactions.append([date, description, float(amount)])

# Convert the extracted data into a DataFrame
df = pd.DataFrame(all_transactions, columns=["Date", "Description", "Amount"])

# Save the combined transactions to an Excel file
df.to_excel(output_excel_file, index=False)

print(f"✅ Extraction complete! {len(all_transactions)} transactions saved to: {output_excel_file}")
