import fitz  # PyMuPDF
import pandas as pd
import re
import os

def parse_po_pdf(pdf_path):
    lines = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text = page.get_text()
            if text:
                lines.extend([line.strip() for line in text.split("\n") if line.strip()])

    parsed_entries = []
    i = 0
    while i < len(lines):
        if "vendor sku" in lines[i].lower():
            try:
                # Skip to after 'Cost'
                while i < len(lines) and "cost" not in lines[i].lower():
                    i += 1
                i += 1

                # Vendor SKU
                vendor_sku_lines = []
                while i < len(lines) and not re.fullmatch(r"\d+", lines[i]):
                    vendor_sku_lines.append(lines[i])
                    i += 1
                vendor_sku = " ".join(vendor_sku_lines)

                # RC SKU
                rc_sku_parts = []
                while i < len(lines) and re.fullmatch(r"\d+", lines[i]):
                    rc_sku_parts.append(lines[i])
                    i += 1
                rc_sku = "".join(rc_sku_parts)

                # Description
                description_lines = []
                while i < len(lines) and lines[i] not in ["XS", "S", "M", "L", "XL"]:
                    description_lines.append(lines[i])
                    i += 1
                description = " ".join(description_lines)

                # Size
                if lines[i] not in ["XS", "S", "M", "L", "XL"]:
                    i += 1
                    continue
                size = lines[i]
                i += 1

                # Vendor Color + Color (1–3 lines)
                color_block = []
                max_color_lines = 3
                lines_remaining = lines[i:i+max_color_lines]
                for line in lines_remaining:
                    if any(word in line.lower() for word in ["style", "totals", "description"]):
                        break
                    color_block.append(line)
                i += len(color_block)

                color_words = " ".join(color_block).split()
                if len(color_words) >= 2:
                    color = " ".join(color_words[-2:])  # last 2 = Color
                    vendor_color = " ".join(color_words[:-2])  # rest = Vendor Color
                else:
                    color = color_words[-1] if color_words else ""
                    vendor_color = ""

                # Qty and Cost (look ahead up to 5 lines)
                qty, cost = None, None
                for j in range(i, min(i + 5, len(lines))):
                    if not qty and re.fullmatch(r"\d+", lines[j]):
                        qty = lines[j]
                    elif not cost and re.search(r"\$?\d+\.\d{2}", lines[j]):
                        cost = re.sub(r"[^0-9.]", "", lines[j])
                    if qty and cost:
                        break
                i = j + 1

                if not (qty and cost):
                    print(f"Skipping incomplete block ending near line {i}")
                    continue

                parsed_entries.append({
                    "Vendor SKU": vendor_sku,
                    "RC SKU": rc_sku,
                    "Description": description,
                    "Size": size,
                    "Vendor Color": vendor_color,
                    "Color": color,
                    "Qty": qty,
                    "Cost": cost
                })

            except Exception as e:
                print(f"Error parsing block at line {i}: {e}")
                i += 1
        else:
            i += 1

    if not parsed_entries:
        print("⚠️ No entries parsed. Check formatting of PDF or keywords like 'Vendor SKU' and 'Cost'.")
    return pd.DataFrame(parsed_entries)


def generate_formatted_description_table(df):
    df["RC SKU"] = df["RC SKU"].astype(str)
    formatted = pd.DataFrame()
    formatted["Description"] = (
        "BRAND: PRINCE PETER COLLECTION\n"
        "DESCRIPTION: " + df["Vendor SKU"] + "\n"
        "C/#: " + df["Vendor Color"] + "\n"
        "RC SKU: " + df["RC SKU"] + "\n"
        + df["Size"] + ' "X" ' + df["Qty"].astype(str)
    )
    formatted["Cost"] = df["Cost"]
    formatted["Qty"] = df["Qty"]
    return formatted


def process_po_pdf_to_excels(pdf_path, output_dir="./"):
    df_structured = parse_po_pdf(pdf_path)
    if df_structured.empty:
        raise ValueError("Parsed table is empty. Please check the PDF formatting.")

    df_formatted = generate_formatted_description_table(df_structured)

    os.makedirs(output_dir, exist_ok=True)
    file1 = os.path.join(output_dir, "Structured_Product_Table.xlsx")
    file2 = os.path.join(output_dir, "Formatted_Description_Table.xlsx")

    df_structured.to_excel(file1, index=False)
    df_formatted.to_excel(file2, index=False)

    return file1, file2


# Example usage
if __name__ == "__main__":
    pdf_path = "scripts/assets/pdf_assets/Rue La La/1049118 Sample.pdf"
    output_dir = "scripts/assets/pdf_assets/Rue La La/"
    structured_file, formatted_file = process_po_pdf_to_excels(pdf_path, output_dir)
    print("Files saved at:")
    print("→ Structured Table:", structured_file)
    print("→ Formatted Description Table:", formatted_file)
