import pdfplumber
import os

# Folder containing PDFs
pdf_folder = "scripts/assets/pdf_assets/cc_statement/Amex/2022 ram delta/"  # Adjust this path
output_folder = "extracted_txt_files/2022 ram delta/"  # Folder to store extracted .txt files

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# List all PDF files in the folder
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_folder, pdf_file)
    output_txt_path = os.path.join(output_folder, pdf_file.replace(".pdf", ".txt"))

    # Extract text from the PDF
    text_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:  # Check if text extraction worked
                text_data.extend(extracted_text.split("\n"))

    # Locate "Total New Charges" and extract everything after it
    start_index = None
    for i, line in enumerate(text_data):
        if "Total New Charges" in line:
            start_index = i + 1  # Text extraction starts after this line
            break

    # Extract relevant text
    if start_index:
        extracted_text = "\n".join(text_data[start_index:])

        # Save extracted text to a .txt file
        with open(output_txt_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        print(f"✅ Extracted and saved: {output_txt_path}")
    else:
        print(f"❌ 'Total New Charges' not found in {pdf_file}. Skipping...")

print("✅ All PDFs processed!")
