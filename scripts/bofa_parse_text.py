import re
import pandas as pd

# Step 1: Load the text file
with open("withdrawals_section.txt", "r") as file:
    text = file.read()

# Step 2: Define the pattern for transactions
# Format: MM/DD/YY [description] -[amount]
pattern = re.compile(r"(\d{2}/\d{2}/\d{2})\s+(.+?)\s+(-\d{1,3}(?:,\d{3})*(?:\.\d{2}))")

# Step 3: Extract matches into a list
matches = pattern.findall(text)
transactions = []

for match in matches:
    date = match[0]
    description = match[1].strip()
    amount = float(match[2].replace(",", ""))
    transactions.append([date, description, amount])

# Step 4: Create a DataFrame
df = pd.DataFrame(transactions, columns=["Date", "Description", "Amount"])
print(df)
# Step 5: Save to Excel
# df.to_excel("parsed_withdrawals.xlsx", index=False)
