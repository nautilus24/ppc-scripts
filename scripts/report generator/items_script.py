import pandas as pd
import re

# Read the Excel file and select the necessary columns
df = pd.read_excel(r'assets\adults_invoice_ytd_61323.xlsx', usecols=['Invoice Number', 'Item Name', 'Item Desc','Customer Name','SubTotal','Quantity',
                                                                     'Item Price', 'Shipping Charge','Invoice Status'])

# Initialize an empty list to store the extracted data
extracted_data = []

# Iterate over the rows in the DataFrame
for _, row in df.iterrows():
    invoice_number = row['Invoice Number']
    item_name = row['Item Name']
    item_desc = row['Item Desc']
    customer_name =  row['Customer Name']
    cost_without_freight = row['SubTotal']
    quantity = row['Quantity']
    item_price = row['Item Price']
    freight = row['Shipping Charge']
    invoice_status = row['Invoice Status']
    
    # Extract item name from Item Desc if Item Name is empty
    if pd.isnull(item_name):
        item_name_match = re.search(r'(?:Description:|Item:|Vendor Item:)(.*?)(?:\n|$)', item_desc, re.IGNORECASE)
        item_name = item_name_match.group(1).strip() if item_name_match else item_desc.split('\n')[0].strip()

    # Remove "PRINCE PETER" from the beginning of item name
    item_name = re.sub(r'^PRINCE PETER\s*', '', item_name)
    
    # Extract color from Item Desc
    color_match = re.search(r'(?:C/#:|C#/:|Color:)\s*(\w+)', item_desc, re.IGNORECASE)
    color = color_match.group(1) if color_match else ''
    
    # Append the extracted data to the list
    extracted_data.append({'Invoice Number': invoice_number, 'Item Name': item_name, 'Color': color, 'Customer': customer_name, 'Cost Without Freight':cost_without_freight, 
                           'Quantity': quantity, 'Item Price': item_price, 'Freight': freight, 'Net Price': (cost_without_freight + freight),'Invoice Status': invoice_status})

# Create a DataFrame from the extracted data
extracted_df = pd.DataFrame(extracted_data)

# Print the extracted data
# print(extracted_df)
df_invoice_to_customer = extracted_df[['Invoice Number', 'Invoice Status', 'Customer', 'Cost Without Freight','Freight']].drop_duplicates().reset_index(drop=True)
# print(df_invoice_to_customer)
df_invoice_to_item = extracted_df[['Invoice Number', 'Item Name','Quantity','Item Price']]
# print(df_invoice_to_item)
extracted_df.to_excel('extracted_data.xlsx', index=False)
