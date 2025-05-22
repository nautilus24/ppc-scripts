import re
import csv

def parse_check_details(text):
    # Regular expression to match date, check number, and amount
    pattern = re.compile(r'(\d{2}/\d{2}/\d{2})\s+(\d+\*?)\s+(-[\d,]+\.\d{2})')

    records = []
    for line in text.split('\n'):  # Split the text into lines
        matches = pattern.findall(line)
        for match in matches:  # match is a tuple (date, check_number, amount)
            # Cleaning and formatting the amount by removing commas
            amount = match[2].replace(',', '')
            records.append([match[0], match[1], amount])

    return records

# Sample data
data = """12/11/23 6041 -1,799.00 12/29/23 6052 -500.0012/08/23 6042 -6,000.00 12/20/23 6053 -270.0012/08/23 6043 -1,000.00 12/27/23 6056* -1,936.0012/11/23 6044 -1,737.00 12/04/23 9001* -5,994.0012/21/23 6045 -1,200.00 12/04/23 9002 -6,153.7412/18/23 6046 -2,778.00 12/14/23 9003 -2,802.2112/18/23 6047 -1,935.00 12/28/23 9004 -279.0012/20/23 6048 -513.00 12/20/23 9006* -5,000.0012/19/23 6049 -100.00 12/28/23 9008* -18,583.5012/19/23 6050 -200.00 12/28/23 9009 -17,767.63
"""

# Parse the data
parsed_data = parse_check_details(data)

# Write the parsed data to a CSV file
csv_filename = 'check_details.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Date', 'Check Number', 'Amount'])
    # Write the data
    for record in parsed_data:
        writer.writerow(record)

print(f"Data written to {csv_filename}")
