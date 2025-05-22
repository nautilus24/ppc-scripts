import pdfplumber
import pandas as pd
import re

# Path to the input PDF
pdf_path = "20210101-statements-4897-.pdf"  # Change this to the actual file path
output_txt = "extracted_text.txt"

# Extract text from the PDF
text_data = []
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            text_data.append(text)

# Save extracted text to a .txt file for manual inspection
with open(output_txt, "w", encoding="utf-8") as f:
    f.write("\n".join(text_data))

print(f"✅ Text extraction complete! File saved as: {output_txt}")