from pdf2image import convert_from_path
import pytesseract
from PIL import Image

def extract_text_from_check_images(pdf_path, start_page, end_page):
    # Convert specific pages of the PDF to images
    images = convert_from_path(pdf_path, first_page=start_page, last_page=end_page)

    all_texts = []

    for image in images:
        text = pytesseract.image_to_string(image)
        all_texts.append(text)

    return all_texts

pdf_path = 'scripts/assets/pdf_assets/data_statement_feb.pdf'
# Extracting from pages 9 to 11
extracted_texts = extract_text_from_check_images(pdf_path, 9, 11)

for idx, text in enumerate(extracted_texts, start=1):
    print(f"Text from Check Image {idx}:\n{text}\n{'='*40}\n")
