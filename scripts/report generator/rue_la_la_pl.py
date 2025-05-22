import pandas as pd
import re

def parse_data(cell):
    # Regular expressions for each field
    patterns = {
        'Vendor SKU': r"VENDOR SKU/#:\s*([^\n]+)",
        'RC SKU': r"RC SKU/#:\s*([^\n]+)",
        'Description': r"DESCRIPTION:\s*([^\n]+)",
        'Size': r"(\bS\b|\bM\b|\bL\b|\bXL\b|\bXS\b)",
        'Vendor Color': r"VENDOR COLOR:\s*([^,\n]+)",  # Adjusted regex for 'Vendor Color'
        'Color': r"\nCOLOR:\s*([^\n]+)",  # Adjusted regex for 'Color'
    }

    # Extract data using regex
    parsed_data = {field: re.search(pattern, cell).group(1) if re.search(pattern, cell) else '' for field, pattern in patterns.items()}

    # Extracting quantity, assuming it follows the size like 'M X 8'
    size_match = re.search(r"(\bS\b|\bM\b|\bL\b|\bXL\b|\bXS\b)\s*X\s*(\d+)", cell)
    if size_match:
        parsed_data['Size'] = size_match.group(1)
        parsed_data['Quantity'] = size_match.group(2)
    else:
        parsed_data['Quantity'] = ''

    return parsed_data

def main():
    # Read Excel file
    file_path = 'scripts/assets/rue la la/data_32024.xlsx'  # Replace with your Excel file path
    df = pd.read_excel(file_path)

    # Assuming the data is in the first column, adjust if necessary
    column_to_parse = df.columns[3]

    # Parse and store the data
    parsed_data = [parse_data(cell) for cell in df[column_to_parse]]
    new_df = pd.DataFrame(parsed_data)

    # Write to CSV
    new_df.to_csv('parsed_data_ruelala.csv', index=False)

if __name__ == "__main__":
    main()
