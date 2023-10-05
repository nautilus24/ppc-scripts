import pandas as pd

# Load the Excel file into a DataFrame
df = pd.read_excel('scripts/assets/data_consignment.xlsx', engine='openpyxl')

# Define the keywords to search for
keywords = ["consignment", "reship", "re-ship"]

# Check each column for the keywords and store the result in a mask
mask = df.apply(lambda col: col.astype(str).str.contains('|'.join(keywords), case=False, na=False)).any()

# Get columns which contain the keywords
matched_columns = mask[mask].index.tolist()

# Extract rows containing these keywords
rows_containing_keywords = df[df.apply(lambda row: row.astype(str).str.contains('|'.join(keywords), case=False, na=False).any(), axis=1)]

# Write the rows containing the keywords to a new Excel file
rows_containing_keywords.to_excel('reship_report.xlsx', index=False, engine='openpyxl')
