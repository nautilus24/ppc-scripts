import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Initialize Selenium WebDriver
def init_driver():
    """Initialize Chrome WebDriver with webdriver-manager."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no UI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920x1080")

    # Automatically download and install ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Google Search for Facebook Page and Extract Email
def get_facebook_email(keyword, driver):
    """Search for the Facebook page and extract emails."""
    try:
        # Step 1: Google search for the Facebook page
        print(f"Searching for: {keyword} Facebook Page")
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(f"{keyword}")
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        # Step 2: Find the first Facebook link
        fb_link = None
        links = driver.find_elements(By.CSS_SELECTOR, "a")
        for link in links:
            href = link.get_attribute("href")
            if href and "facebook.com" in href:
                fb_link = href
                break

        if not fb_link:
            print(f"No Facebook page found for {keyword}")
            return None, "No Facebook Page Found"

        print(f"Found Facebook Page: {fb_link}")
        driver.get(fb_link)
        time.sleep(5)  # Wait for page to load

        # Step 3: Extract email addresses
        page_source = driver.page_source
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", page_source)

        if emails:
            return fb_link, ', '.join(set(emails))
        else:
            return fb_link, "No Email Found"
    except Exception as e:
        print(f"Error processing {keyword}: {e}")
        return None, "Error"

# Main Function
def main():
    input_file = "scripts/assets/data_boutique_final.xlsx"  # Input Excel file
    output_file = "output_with_emails.xlsx"  # Output Excel file

    # Load input file
    df = pd.read_excel(input_file)
    if 'Facebook Page' not in df.columns:
        df['Facebook Page'] = ''
    if 'Email' not in df.columns:
        df['Email'] = ''

    # Initialize WebDriver
    driver = init_driver()

    # Process each keyword
    for index, row in df.iterrows():
        keyword = row['keyword']
        fb_link, email = get_facebook_email(keyword, driver)
        df.at[index, 'Facebook Page'] = fb_link
        df.at[index, 'Email'] = email

        # Save progress after each row
        df.to_excel(output_file, index=False)
        print(f"Processed: {keyword} -> {email}")

    driver.quit()
    print("Processing complete. Results saved to output_with_emails.xlsx")

if __name__ == "__main__":
    main()
