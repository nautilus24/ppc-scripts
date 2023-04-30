import csv

# Specify the name of the input CSV file
input_file_path = 'scripts/assets/commissions/invoice_numbers_cleaned.csv'

# Specify the name of the output CSV file
output_file_path = 'scripts/assets/commissions/invoice_numbers_numeric.csv'

# Open the input CSV file and create the output CSV file
with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
    csv_reader = csv.reader(input_file)
    csv_writer = csv.writer(output_file)

    # Write the header row to the output CSV file
    csv_writer.writerow(['Invoice Number', 'Processed Invoice Number'])

    # Loop through each row of the input CSV file and process the invoice number
    for row in csv_reader:
        # Extract the digits from the invoice number using regex
        invoice_number = ''.join(filter(str.isdigit, row[0]))

        # Determine the processing to apply based on the length of the digits
        if len(invoice_number) == 4 and invoice_number.startswith('1'):
            processed_invoice_number = 'INV-' + '00' + invoice_number
        elif len(invoice_number) == 3:
            processed_invoice_number = 'INV-' + '000' + invoice_number
        else:
            processed_invoice_number = 'INV-' + invoice_number

        # Write the original and processed invoice numbers to the output CSV file
        csv_writer.writerow([row[0], processed_invoice_number])
