import pandas as pd

# Sample data (replace this with your actual data)
data = """
Line No Item No Vendor ID Qty
Ordered
Unit of
Measure
Qty per
Carton Price Ext.
Price
1 810133286857 PPCKIDSSP1802 2 EA 8.00 16.00
Price Type Code : WE | Retail Price : 28
2 810133286819 PPCGRLSBRB1103 2 EA 9.50 19.00
Price Type Code : WE | Retail Price : 28
3 810133286864 PPCKIDSSP1802 4 EA 8.00 32.00
Price Type Code : WE | Retail Price : 28
4 810133286826 PPCGRLSBRB1103 4 EA 9.50 38.00
Price Type Code : WE | Retail Price : 28
5 810133286871 PPCKIDSSP1802 4 EA 8.00 32.00
Price Type Code : WE | Retail Price : 28
6 810133286833 810133286833 4 EA 9.50 38.00
Price Type Code : WE | Vendor's Style Number : PPCGRLSBRB1103 | Retail Price : 28
7 810133286888 810133286888 2 EA 8.00 16.00
Price Type Code : WE | Vendor's Style Number : PPCKIDSSP1802 | Retail Price : 28
8 810133286840 PPCGRLSBRB1103 2 EA 9.50 19.00
Price Type Code : WE | Retail Price : 28
9 810133286895 PPCKDSSP400 2 EA 8.00 16.00
10 810087789978 PPCKIDSSP11402 2 EA 9.50 19.00
Price Type Code : WE | Retail Price : 28
11 810133286901 PPCKDSSP400 4 EA 8.00 32.00
Price Type Code : WE | Retail Price : 28
12 810087789985 PPCKIDSSP11402 4 EA 9.50 38.00
Price Type Code : WE | Retail Price : 28
13 810133286918 PPCKDSSP400 4 EA 8.00 32.00
Price Type Code : WE | Retail Price : 28
14 810087789992 PPCKIDSSP11402 4 EA 9.50 38.00
Price Type Code : WE | Retail Price : 28
15 810133286925 810133286925 2 EA 8.00 16.00
Price Type Code : WE | Vendor's Style Number : PPCKDSSP400 | Retail Price : 28
16 810133280008 PPCKIDSSP11402 2 EA 9.50 19.00
Price Type Code : WE | Retail Price : 28
17 810133286970 PPCGRLSBRB701 2 EA 8.00 16.00
Price Type Code : WE | Retail Price : 28
18 810133286987 PPCGRLSBRB701 4 EA 8.00 32.00
Price Type Code : WE | Retail Price : 28
19 810133286994 PPCGRLSBRB701 4 EA 8.00 32.00
Price Type Code : WE | Retail Price : 28
20 810133287007 PPCGRLSBRB701 2 EA 8.00 16.00"""

# Split the data into lines
lines = data.strip().split('\n')

# Initialize variables
rows = []
current_row = []

for line in lines:
    if line.strip().split()[0].isdigit():  # Checks if the line starts with a digit
        if current_row:
            rows.append(current_row)
        current_row = [line]
    else:
        current_row.append(line)

# Append the last row
if current_row:
    rows.append(current_row)

# Process each row
processed_data = []

for row in rows:
    # Assuming each row has a fixed number of columns
    # Modify the slicing as per the actual data structure
    line_no, item_no, vendor_id, qty, unit, price, ext_price = row[0].split()[:7]
    additional_info = ' '.join(row[0].split()[7:]) + ' ' + ' '.join(row[1:])
    processed_data.append([line_no, item_no, vendor_id, qty, unit, price, ext_price, additional_info])

# Create a DataFrame
df = pd.DataFrame(processed_data, columns=['Line No', 'Item No', 'Vendor ID', 'Qty', 'Unit of Measure', 'Price', 'Ext. Price', 'Additional Info'])

# Export to Excel
df.to_excel('belk.xlsx', index=False)
