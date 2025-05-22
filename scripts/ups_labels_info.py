import fitz  # PyMuPDF
import pandas as pd

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def parse_ups_labels(text):
    import re
    ship_to_pattern = r"Ship To:\s*(.*)"
    reference_pattern = r"Reference #1:\s*(.*)"
    tracking_pattern = r"Tracking #:\s*(.*)"

    ship_to_list = re.findall(ship_to_pattern, text)
    reference_list = re.findall(reference_pattern, text)
    tracking_list = re.findall(tracking_pattern, text)

    return ship_to_list, reference_list, tracking_list

def save_to_excel(ship_to_list, reference_list, tracking_list, output_path):
    df = pd.DataFrame({
        'SHIP TO:': ship_to_list,
        'Reference #1:': reference_list,
        'TRACKING #:': tracking_list
    })
    df.to_excel(output_path, index=False)
    


# Paths
pdf_path = "scripts/assets/FAB'RIK 5.15.2024 LABELS.pdf"
output_path = 'output_labels.xlsx'

# Process
text = extract_text_from_pdf(pdf_path)
print(text)
ship_to_list, reference_list, tracking_list = parse_ups_labels(text)
save_to_excel(ship_to_list, reference_list, tracking_list, output_path)
# print(df)

print("Extraction and saving to Excel completed.")
