import pandas as pd

# Read the Excel file into a pandas DataFrame
file_path = 'scripts/report generator/assets/data_boutiques.xlsx'
df = pd.read_excel(file_path, skiprows=3)

# Split the "Notes" column into individual item-color pairs
item_color_pairs = df['Notes'].str.split(', ')

# Initialize lists to store extracted items and colors
items = []
colors = []

# Loop through each item-color pair and extract items and colors
for pair_list in item_color_pairs:
    for pair in pair_list:
        item_color = pair.rsplit(' ', 1)
        item = ' '.join(item_color[:-1])
        color = item_color[-1]
        items.append(item)
        colors.append(color)
        
items_df = pd.DataFrame({'Items': items})

# Group by item names and calculate the count
item_counts = items_df['Items'].value_counts().reset_index()
item_counts.columns = ['Item', 'Count']

# Print the resulting DataFrame
print(item_counts)