import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re
import pandas as pd
import time


def scrape_emails_from_website(url):
    """Scrape clean email addresses from a given website URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract potential email addresses
        raw_emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', soup.get_text()))
        # Validate emails (remove unwanted concatenated text)
        clean_emails = {email for email in raw_emails if '@' in email and '.' in email.split('@')[-1]}
        return clean_emails
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return set()


def find_website_for_one_shop(shop_name, city_name, state=None):
    """Perform Google search and get the first result URL."""
    query = f"{shop_name} {city_name}"
    if state:
        query += f" {state}"
    query += " email address"

    print(f"Searching for: {query}")
    
    try:
        for url in search(query, num_results=1):
            print(f"First result URL: {url}")
            return url
        print("No results found.")
        return None
    except Exception as e:
        print(f"Google search failed: {e}")
        return None

def main():
    # Read data from Excel file
    df = pd.read_excel("scripts/assets/data_non_boutique.xlsx")

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # if index >= 10:
        #     break
        shop_name = row['Shop Name']
        city_name = row['City']
        state = row.get('State', None)  # Handle missing state values

        try:
            url = find_website_for_one_shop(shop_name, city_name, state)
            if url:
                df.at[index, 'Website'] = url
                emails = scrape_emails_from_website(url)
                if emails:
                    df.at[index, 'Email'] = ', '.join(emails)
        except Exception as e:
            print(f"Error processing {shop_name}: {str(e)}")

        # Implement a backoff mechanism to respect Google Search API rate limits
        time.sleep(2)

    # Save the modified DataFrame to a new Excel file
    df.to_excel('output_boutique_v2.xlsx', index=False)

if __name__ == "__main__":
    main()