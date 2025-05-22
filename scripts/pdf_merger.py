import os
from PyPDF2 import PdfMerger

# Define the path to the folder containing the PDFs
folder_path = 'C:/Users/priya/OneDrive/Documents/Home Depot Receipts Year - 2022/Home Depot Receipts Year - 2022'

# Create a PdfMerger object
merger = PdfMerger()

# Iterate over all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.pdf'):
        filepath = os.path.join(folder_path, filename)
        # Append each PDF file to the merger object
        merger.append(filepath)

# Define the output path for the combined PDF
output_path = os.path.join(folder_path, 'combined_output.pdf')

# Write the merged PDF to a file
with open(output_path, 'wb') as output_pdf:
    merger.write(output_pdf)

# Close the merger
merger.close()

print(f"Combined PDF saved to: {output_path}")
