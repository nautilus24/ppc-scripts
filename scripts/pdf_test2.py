import pandas as pd

# Define the Excel file path
file_path = 'scripts/assets/ppc_ss_pdfReport.xlsx'

# Load the Excel file
xls = pd.ExcelFile(file_path)

# Read each sheet into a separate DataFrame and store them in a list
all_data = [xls.parse(sheet_name) for sheet_name in xls.sheet_names]

# Concatenate all the DataFrames in the list into a single DataFrame
combined_data = pd.concat(all_data, ignore_index=True)

print(combined_data.columns)

# Ensure each column involved in the concatenation is a string
combined_data['Concatenated'] = combined_data[' Description'].astype(str) + ', ' + \
                                combined_data['Color'].astype(str) + ',Size= ' + \
                                combined_data['Size'].astype(str)

unique_items = combined_data.groupby('Item').agg({
    'Concatenated': 'first'  # Take the first value since they are the same for all in each group
}).reset_index()

output_path = 'scripts/assets/unique_items_output.xlsx'
unique_items.to_excel(output_path, index=False)

print(f"Data has been written to {output_path}")