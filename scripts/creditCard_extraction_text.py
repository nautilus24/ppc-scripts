import pandas as pd
import re

# Define the path to the extracted text file
input_text_file = "extracted_txt_files/18_11.txt"  # Change this to your actual file path
output_excel_file = "Formatted_Transactions.xlsx"

# Read the text file
with open(input_text_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Initialize a list to store transactions
transactions = []

# Regular expression to detect a transaction entry (Date + Description + Amount)
transaction_pattern = re.compile(r"(\d{2}/\d{2}/\d{2})\s+(.+?)\s+\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)")

# Iterate over the lines and extract transactions
for line in lines:
    match = transaction_pattern.search(line)
    if match:
        date = match.group(1)
        description = match.group(2).strip()
        amount = match.group(3).replace(",", "")  # Remove commas for numerical consistency
        transactions.append([date, description, float(amount)])

# Convert the extracted data into a DataFrame
df = pd.DataFrame(transactions, columns=["Date", "Description", "Amount"])
# print (df)
# Save the extracted transactions to an Excel file
df.to_excel(output_excel_file, index=False)

print(f"✅ Extraction complete! File saved as: {output_excel_file}")
