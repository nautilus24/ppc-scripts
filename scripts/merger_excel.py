import pandas as pd
import os

# Folder path where all Excel files are stored
folder_path = "scripts/assets/merger_files/CassetteTapeMuscleTank"

# Get a list of all Excel files in the folder
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx') or f.endswith('.xls')]

# Create an empty list to store dataframes
dfs = []

for file in excel_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_excel(file_path)  # Read each Excel file
    dfs.append(df)

# Combine all dataframes into one
combined_df = pd.concat(dfs, ignore_index=True)

# Save to a new Excel file
combined_df.to_excel("merged_file.xlsx", index=False)

print("Files combined successfully!")
