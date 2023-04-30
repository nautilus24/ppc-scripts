import csv

# Specify the name of the input CSV file
input_file_path = 'scripts/assets/commissions/invoice_numbers_raw.csv'

# Specify the name of the output CSV file
output_file_path = 'scripts/assets/commissions/invoice_numbers_cleaned.csv'

# Open the input CSV file and create the output CSV file
with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
    csv_reader = csv.reader(input_file)
    csv_writer = csv.writer(output_file)

    # Write the header row to the output CSV file
    csv_writer.writerow(['Invoice Number'])

    # Loop through each row of the input CSV file and clean the invoice number
    for row in csv_reader:
        # Get the raw invoice number from the input CSV file
        raw_invoice_number = row[0]

        # Split the invoice number on the '&' character
        invoice_numbers = raw_invoice_number.split('&')

        # Loop through each invoice number and clean it
        for invoice_number in invoice_numbers:
            # Check if the invoice number contains a range (e.g. INV 765 - INV 770)
            if '-' in invoice_number:
                # Split the range on the '-' character
                start, end = invoice_number.split('-')

                # Extract the numeric parts of the start and end of the range
                start_number = int(start.split()[-1])
                end_number = int(end.split()[-1])

                # Generate a list of invoice numbers from the start to the end of the range
                range_invoice_numbers = [f"{start.split()[0]} {i}" for i in range(start_number, end_number+1)]

                # Write each invoice number in the range to the output CSV file
                for range_invoice_number in range_invoice_numbers:
                    csv_writer.writerow([range_invoice_number])
            else:
                # Write the cleaned invoice number to the output CSV file
                invoice_number = invoice_number.strip()
                csv_writer.writerow([invoice_number])
