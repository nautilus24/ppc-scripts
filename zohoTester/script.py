import requests

# Define the API endpoints and credentials
base_url = "https://invoice.zoho.com/api/v3"
client_id = "1000.6ZY5RV7TCTZGWSNB68R14K7UZC0TQQ"
client_secret = "8f13952c81ddafecffcb3e0dc0b1f75d28e83bdbcf"

# Get the access token
def get_access_token():
    url = f"{base_url}/oauth/v2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "InvoiceAPI.invoices.READ"  # Adjust the scope based on the required access
    }
    response = requests.post(url, data=payload)
    access_token = response.json().get("access_token")
    return access_token

# Fetch invoice data
def fetch_invoice_data():
    access_token = get_access_token()
    url = f"{base_url}/invoices"
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }
    response = requests.get(url, headers=headers)
    invoice_data = response.json()
    return invoice_data

# Main execution
if __name__ == "__main__":
    invoice_data = fetch_invoice_data()
    print(invoice_data)
