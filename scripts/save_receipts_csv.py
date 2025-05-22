import csv
from e_receipt_reader_multi import process_all_pdfs

def write_receipts_to_csv(receipts, csv_filename):
    # Define the header
    header = ["filename", "location", "date", "total_amount"]
    
    # Write data to CSV file
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for receipt in receipts:
            writer.writerow(receipt)
    
    print(f"Data successfully written to {csv_filename}")

if __name__ == "__main__":
    # Directory containing all PDF files
    directory_path = "C:/Users/priya/PycharmProjects/PPC/scripts/assets/pdf_assets/e-recipts/"
    
    # Process all receipts
    receipts = process_all_pdfs(directory_path)
    
    # Write the processed data to a CSV file
    csv_filename = "receipts_output.csv"
    write_receipts_to_csv(receipts, csv_filename)
