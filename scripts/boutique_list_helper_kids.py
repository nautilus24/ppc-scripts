import pandas as pd
import re

# Use a raw string literal for the file path
file_path = r'scripts/assets/data_kids.xlsx'

# Read the Excel file
df = pd.read_excel(file_path, header=0)
df['Item Name'] = df['Item Name'].fillna('')
df['SubTotal'] = '$' + df['SubTotal'].astype(str)

# Define a function to extract the color from the 'Item Desc' column
def extract_color(desc):
    # Regular expression to match color patternsq
    pattern = r'(C/#:|Color:|C#/:)\s*(.*?)(\n|$)'
    match = re.search(pattern, desc, flags=re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(2).strip()
    else:
        return ''

# Define a function to extract the item name from the 'Item Desc' column when 'Item Name' is blank
def extract_item_name(row):
    if row['Item Name']:
        return row['Item Name']
    desc = row['Item Desc']
    # Look for 'Description:' in the description
    pattern = r'Description:(.*)'
    match = re.search(pattern, desc, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # If 'Description:' not found, take the first line of the description as item name
    first_line = desc.split('\n')[0].strip()
    if first_line:
        return first_line
    # If the first line is empty, return empty string
    return ''

# Apply the function to create a new 'Item Name' column when 'Item Name' is blank
df['Item Name'] = df.apply(extract_item_name, axis=1)

# Apply the function to create a new 'Color' column
df['Color'] = df['Item Desc'].apply(extract_color)

# Concatenate the 'Item Name' and 'Color' columns to create a new 'Item Description' column
df['Item Description'] = df['Item Name'] + ' ' + df['Color']

# Group the data by 'Invoice Number' and 'Invoice Date', and aggregate the 'Item Description' column using join() function with separator ','
grouped_data = df.groupby(['Invoice Number', 'Invoice Status', 'Invoice Date', 'Customer Name', 'PurchaseOrder', 'SubTotal'])['Item Description'].agg(lambda x: ', '.join(x)).reset_index()

# Split the data into two dataframes based on invoice status
draft_invoices = grouped_data[grouped_data['Invoice Status'] == 'Draft']
approved_invoices = grouped_data[grouped_data['Invoice Status'] != 'Draft']

# Output the contents of the draft invoices dataframe to Excel
draft_invoices.to_excel('draft_invoices_kids.xlsx', index=False)

# Output the contents of the approved invoices dataframe to Excel
# approved_invoices.to_excel('approved_invoices.xlsx', index=False)
