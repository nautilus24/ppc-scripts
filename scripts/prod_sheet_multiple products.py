import pandas as pd
file_path = 'scripts/assets/production_sheet_kids/data_adults_2024_2025YTD.xlsx'
df = pd.read_excel(file_path)
# print(df.head())
product_codes = ["PPC-TSET101","PPC-TSET102","PPC-TSET201","PPC-TSET202","PPC-BTS1301","PPC-BTS102","PPC-BTS1401","PPC-BTS1402","PPC-BTS101","PPC-BTS1001","PPC-BTS601",
                 "PPC-BTS202","PPC-BTS802","PPC-BTS302","PPC-BTS401","PPC-BTS1102","PPC-BTS501","PPC-BTS701","PPC-BTS1202","PPC-BTS602","PPC-BTS801","PPC-BTS201","PPC-BTS402","PPC-BTS902",
                 "PPC-BTS1002","PPC-BTS1101","PPC-BTS301","PPC-BTS1201","PPC-BTS901","PPC-BTS800","PPC-BTS900"]
product_codes_temp=["Florida Distressed Crop","Florida","Gameday","Alabama","Tennessee","Georgia","Miami","Ringer"]
# filtered_df = df[df['Item Desc'].str.contains("|".join(product_codes_temp), case=False, na=False) & 
#                  (df['Invoice Status'] == 'Closed') | (df['Invoice Status'] == 'Draft')].copy()
filtered_df = df[df['Item Desc'].str.contains("|".join(product_codes_temp), case=False, na=False) & 
                 (df['Invoice Status'] == 'Closed')].copy()

def extract_size_count(desc, pattern):
    import re
    match = re.search(f"{pattern} (\d+)", desc)
    return int(match.group(1)) if match else 0

filtered_df['XS'] = filtered_df['Item Desc'].apply(lambda x: extract_size_count(x, 'XS X'))
filtered_df['S'] = filtered_df['Item Desc'].apply(lambda x: extract_size_count(x, 'S X'))
filtered_df['M'] = filtered_df['Item Desc'].apply(lambda x: extract_size_count(x, 'M X'))
filtered_df['L'] = filtered_df['Item Desc'].apply(lambda x: extract_size_count(x, 'L X'))
filtered_df['XL'] = filtered_df['Item Desc'].apply(lambda x: extract_size_count(x, 'XL X'))

result_df = filtered_df[['Customer Name', 'Invoice Number','Item Name' ,'XS','S', 'M', 'L', 'XL','Item Price']]
# Calculate Total Qty as the sum of XS, S, M, L, and XL columns
result_df['Total Qty'] = result_df[['XS', 'S', 'M', 'L', 'XL']].sum(axis=1)

# Calculate Net Cost as Item Price * Total Qty
result_df['Net Cost'] = result_df['Item Price'] * result_df['Total Qty']

# print(result_df.isna().any().any())
sorted_df = result_df.sort_values(by='Item Name')
result_array = sorted_df.values

print(result_array)

output_file_path = 'production_sheet.xlsx'
result_df.to_excel(output_file_path, index=False, engine='openpyxl')