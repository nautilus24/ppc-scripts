import re
import csv

def parse_bank_statement(text):
    # Regular expression to identify date patterns and split the text
    pattern = re.compile(r'(\d{2}/\d{2}/\d{2})')
    parts = pattern.split(text)[1:]  # Split and ignore the first empty string

    records = []
    for i in range(0, len(parts), 2):
        date = parts[i]
        rest = parts[i + 1]
        
        # Further split to separate the amount and description
        match = re.search(r'(\d[\d,]*\.\d{2})', rest)
        if match:
            amount = match.group(1)
            description = rest[:match.start()].strip()
            records.append([date, description, amount])

    return records

# Sample data
data = """
12/01/23 953340419 12/01 #000015946 WITHDRWL SUPERFOOD PLAZA
ORANJESTAD FEE CKCD XXXXXXXXXXXX5049
-5.0012/05/23 Prfd Rwds for Bus-Intl Wire Fee Waiver of $15 -0.0012/18/23 3 RUE LA BOETI 12/17 #000755052 WITHDRWL 497100300560050
PARIS CKCD XXXXXXXXXXXX5049 INTERNATIONAL TRANSACTION FEE
-9.9112/18/23 3 RUE LA BOETI 12/17 #000755052 WITHDRWL 497100300560050
PARIS FEE CKCD XXXXXXXXXXXX5049
-5.0012/21/23 Prfd Rwds for Bus-Wire Fee Waiver of $15 -0.00
"""

# Parse the data
parsed_data = parse_bank_statement(data)

# Display the parsed data
# for record in parsed_data:
#     print(record)
csv_filename = 'bank_statement.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Date', 'Description', 'Amount'])
    # Write the data
    for record in parsed_data:
        writer.writerow(record)

print(f"Data written to {csv_filename}")