# data = pd.read_excel("scripts/assets/data_statement_jan.xlsx", header=None)
import pandas as pd

# Load the Excel file and the 'Income' tab
data = pd.read_excel("scripts/assets/data_statement_jan.xlsx", sheet_name="income", header=None)

# Split the combined column (column 0) into 'Date' and 'Description'
data['Date'] = data[0].str.extract(r'(\d{2}/\d{2}/\d{2})')
data['Description'] = data[0].str.replace(r'\d{2}/\d{2}/\d{2}', '', regex=True).str.strip()

# Drop the original combined column
data.drop(columns=[0], inplace=True)

# Rename the amount column
data.rename(columns={1: 'Amount'}, inplace=True)

# Rearrange columns to have 'Date', 'Description', and then 'Amount'
data = data[['Date', 'Description', 'Amount']]

# Save the transformed dataframe back to the same Excel file in 'Income' tab
with pd.ExcelWriter("path_to_your_file.xlsx", engine='openpyxl', mode='a') as writer:
    data.to_excel(writer, sheet_name='Income', index=False, header=['Date', 'Description', 'Amount'])

