import csv

# Specify the name of the input CSV file
input_file_path = 'scripts/assets/data_square_april.csv'

# Specify the name of the output CSV file
output_file_path = 'scripts/assets/commissions/invoice_numbers_raw.csv'

# Specify the name of the column containing the invoice numbers
invoice_column_name = 'Description' # replace with the name of your desired column

# Open the input CSV file and create the output CSV file
with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
    csv_reader = csv.DictReader(input_file)
    csv_writer = csv.writer(output_file)

    # Write the header row to the output CSV file
    csv_writer.writerow(['Invoice Number'])

    # Loop through each row of the input CSV file and extract the invoice number
    for row in csv_reader:
        # Get the invoice number from the specified column
        invoice_number = None
        if 'inv' in row[invoice_column_name].lower():
            invoice_number = row[invoice_column_name][row[invoice_column_name].lower().find('inv'):]

        # Write the invoice number to the output CSV file
        if invoice_number:
            csv_writer.writerow([invoice_number])
