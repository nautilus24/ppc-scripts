import csv

# Specify the name of the input CSV file
input_file_path = 'scripts/assets/commissions/invoice_numbers_numeric.csv'

# Specify the name of the output CSV file
output_file_path = 'scripts/assets/commissions/invoice_numbers_processed.csv'

# Open the input CSV file and create the output CSV file
with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
    csv_reader = csv.reader(input_file)
    csv_writer = csv.writer(output_file)

    # Write the header row to the output CSV file
    csv_writer.writerow(['Invoice Number', 'Processed Invoice Number', 'Type'])

    # Loop through each row of the input CSV file and process the invoice number
    for row in csv_reader:
        processed_invoice_number = row[1]
        if processed_invoice_number.startswith('INV-0'):
            invoice_type = 'Kids'
        else:
            invoice_type = 'Adults'

        # Write the original invoice number, processed invoice number, and type to the output CSV file
        csv_writer.writerow([row[0], row[1], invoice_type])
