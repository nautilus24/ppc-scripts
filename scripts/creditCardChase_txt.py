import pandas as pd
import re

# Path to the extracted text file
input_text_file = "extracted_text.txt"  # Change this to match your file
output_excel_file = "Filtered_Positive_Transactions.xlsx"

# Read the text file
with open(input_text_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Locate "PAYMENTS AND OTHER CREDITS" section
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
        match = re.search(r"(\d{2}/\d{2})\s+(.+?)\s+(\d{1,3}(?:,\d{3})*\.\d{2})$", line.strip())

        if match:
            date = match.group(1)
            description = match.group(2).strip()
            amount = match.group(3).replace(",", "")  # Remove commas for numerical consistency

            # Handle multi-line descriptions (merge buffer)
            if buffer:
                description = " ".join(buffer) + " " + description
                buffer = []  # Reset buffer

            # Convert to float and add only positive amounts
            if float(amount) > 0:
                transactions.append([date, description, float(amount)])

        else:
            # If a line doesn't match, assume it's part of a multi-line description
            if line.strip():
                buffer.append(line.strip())

# Convert to DataFrame
df = pd.DataFrame(transactions, columns=["Date", "Description", "Amount"])

# Display extracted data
print(df)

# # Save extracted transactions to an Excel file
# df.to_excel(output_excel_file, index=False)

# print(f"✅ Extraction complete! File saved as: {output_excel_file}")
