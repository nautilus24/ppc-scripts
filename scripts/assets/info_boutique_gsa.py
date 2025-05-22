import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from googleapiclient.discovery import build
from concurrent.futures import ThreadPoolExecutor
import re

# Logging Configuration
logging.basicConfig(level=logging.INFO, filename="scraping.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Constants (Replace with your own API key and Custom Search Engine ID)
GOOGLE_API_KEY = "AIzaSyBmzPYp843N7m080b5GvOVF0v-sHhzVAqQ"
CSE_ID = "e2a877dc375ca4dcb"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Initialize Google Search API
def google_search(query, num_results=1):
    """Search Google using the Custom Search API."""
    try:
        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
        result = service.cse().list(q=query, cx=CSE_ID, num=num_results).execute()
        return result.get("items", [])[0].get("link", None) if result.get("items") else None
    except Exception as e:
        logging.error(f"Google search failed for query '{query}': {e}")
        return None

# Scrape Emails from Website
def scrape_emails_from_website(url):
    """Scrape and validate email addresses from a website."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', soup.get_text()))
        return {email for email in emails if '@' in email}
    except requests.RequestException as e:
        logging.warning(f"Failed to fetch {url}: {e}")
        return set()

# Facebook Search as Fallback
def search_facebook_page(shop_name, city_name):
    """Construct a Facebook search URL."""
    search_query = f"https://www.facebook.com/search/top/?q={shop_name} {city_name}"
    logging.info(f"Fallback to Facebook: {search_query}")
    return search_query

# Process Each Store
def process_store(index, row, df):
    shop_name = row['Shop Name']
    city_name = row['City']
    state = row.get('State', '')
    query = f"{shop_name} {city_name} {state} email address"

    try:
        # Skip rows with existing data
        if pd.notna(row['Website']):
            return

        # Google Search for Website
        url = google_search(query)
        if url:
            df.at[index, 'Website'] = url
            emails = scrape_emails_from_website(url)
            if emails:
                df.at[index, 'Email'] = ', '.join(emails)
        else:
            # Fallback to Facebook Search
            fb_url = search_facebook_page(shop_name, city_name)
            df.at[index, 'Website'] = fb_url
            df.at[index, 'Email'] = 'Manual Check Required'
    except Exception as e:
        logging.error(f"Error processing {shop_name}: {e}")
    time.sleep(1)  # To avoid hitting rate limits

# Main Function
def main():
    input_file = "scripts/assets/data_non_boutique_v2.xlsx"
    output_file = "output_boutique_v3.xlsx"
    batch_size = 10
    
    # Load Data
    df = pd.read_excel(input_file)
    if 'Website' not in df.columns:
        df['Website'] = ''
    if 'Email' not in df.columns:
        df['Email'] = ''
    
    total_rows = len(df)
    
    # Process Stores in Batches
    for start in range(0, total_rows, batch_size):
        end = start + batch_size
        logging.info(f"Processing rows {start} to {min(end, total_rows)}")
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_store, index, row, df) for index, row in df.iloc[start:end].iterrows()]
            for future in futures:
                future.result()
        
        # Save progress after every batch
        df.to_excel(output_file, index=False)
        logging.info(f"Batch {start} to {min(end, total_rows)} saved.")
        print(f"Processed rows {start} to {min(end, total_rows)}")
        
    logging.info("Processing complete. Results saved.")
    print("Processing complete. Results saved.")

if __name__ == "__main__":
    main()
