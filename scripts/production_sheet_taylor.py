import pandas as pd
import re

file_path = 'scripts/assets/production_sheet_kids/data_adults_61924.xlsx'
df = pd.read_excel(file_path)

# List of product names to filter
product_names = ["Taylor"]

# Filter the DataFrame based on product names in the 'Item Name' column and Invoice Status not equal to 'Paid'
filtered_df = df[(df['Item Name'].str.contains("|".join(product_names), case=False, na=False)) & 
                 (df['Invoice Status'] != 'Closed') & (df['Invoice Status'] != 'Void')].copy()


# Function to extract size counts from the description
def extract_size_count(desc, pattern):
    match = re.search(f"{pattern} (\d+)", desc)
    return int(match.group(1)) if match else 0

# Apply the function to extract size counts and create new columns
filtered_df['XS'] = filtered_df['Item Desc'].apply(lambda x: extract_size_count(x, 'XS X'))
filtered_df['S'] = filtered_df['Item Desc'].apply(lambda x: extract_size_count(x, 'S X'))
filtered_df['M'] = filtered_df['Item Desc'].apply(lambda x: extract_size_count(x, 'M X'))
filtered_df['L'] = filtered_df['Item Desc'].apply(lambda x: extract_size_count(x, 'L X'))
filtered_df['XL'] = filtered_df['Item Desc'].apply(lambda x: extract_size_count(x, 'XL X'))

# Prepare the result DataFrame with the required columns
result_df = filtered_df[['Customer Name', 'Invoice Number', 'Item Name', 'XS', 'S', 'M', 'L', 'XL']]

# Sort the result DataFrame by 'Item Name'
sorted_df = result_df.sort_values(by='Item Name')

# Convert the sorted DataFrame to a NumPy array and print it
result_array = sorted_df.values
print(result_array)

# Export the result DataFrame to an Excel file
output_file_path = 'production_sheet.xlsx'
result_df.to_excel(output_file_path, index=False, engine='openpyxl')
