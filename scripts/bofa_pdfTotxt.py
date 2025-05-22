import pdfplumber

# Step 1: Path to your PDF file
pdf_path = "eStmt_2018-01-31 (1).pdf"

# Step 2: Initialize variables
withdrawals_text = []
start_extracting = False

# Step 3: Open the PDF and read each page
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if "Withdrawals and other debits" in text:
            start_extracting = True
        if start_extracting:
            withdrawals_text.append(text)

# Step 4: Extract only the relevant part of the text
all_text = "\n".join(withdrawals_text)
start_index = all_text.find("Withdrawals and other debits")
extracted_text = all_text[start_index:]

# Step 5: Save to text file
with open("withdrawals_section.txt", "w") as file:
    file.write(extracted_text)
