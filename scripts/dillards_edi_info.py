from PyPDF2 import PdfReader

# Path to the uploaded PDF
pdf_path = "scripts/report generator/LM41115170004_480992AA_LBLRE_997DILLARD-1.pdf"

# Extract text from the PDF
def extract_text_from_pdf(pdf_path):
    all_text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            all_text += page.extract_text() + "\n"
    except Exception as e:
        all_text = f"Error reading PDF: {e}"
    return all_text

# Extract text
text = extract_text_from_pdf(pdf_path)
print(text)
# Save the extracted text to a file for review
output_path = "output_text.txt"
with open(output_path, "w", encoding="utf-8") as file:
    file.write(text)

output_path

