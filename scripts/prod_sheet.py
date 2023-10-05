import pandas as pd
file_path = 'scripts/assets/production_sheet_kids/data_10523.csv'
df = pd.read_csv(file_path)
# print(df.head())
filtered_df = df[df['Item Desc'].str.contains('BESTIE REPEAT', case=False, na=False)].copy()

def extract_size_count(desc, pattern):
    import re
    match = re.search(f"{pattern} (\d+)", desc)
    return int(match.group(1)) if match else 0

filtered_df['S'] = filtered_df['Item Desc'].apply(lambda x: extract_size_count(x, 'S X'))
filtered_df['M'] = filtered_df['Item Desc'].apply(lambda x: extract_size_count(x, 'M X'))
filtered_df['L'] = filtered_df['Item Desc'].apply(lambda x: extract_size_count(x, 'L X'))
filtered_df['XL'] = filtered_df['Item Desc'].apply(lambda x: extract_size_count(x, 'XL X'))

result_df = filtered_df[['Customer Name', 'Invoice Number','Item Name' ,'S', 'M', 'L', 'XL']]
# print(result_df.isna().any().any())
sorted_df = result_df.sort_values(by='Item Name')
result_array = sorted_df.values

print(result_array)

output_file_path = 'production_sheet.xlsx'
result_df.to_excel(output_file_path, index=False, engine='openpyxl')