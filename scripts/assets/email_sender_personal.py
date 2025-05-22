import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import time

# Email credentials
# Email credentials
EMAIL_ADDRESS = "princepetercollection1@gmail.com"  # Replace with your Gmail
EMAIL_PASSWORD = "jpid nwyc ioah kqit"  # Replace with your app-specific password

# Email settings
SUBJECT = "Dallas Show - Welcome Offer"
IMAGE_PATH = "C:/Users/priya/Downloads/Dallas_Flyer.jpg"  # Replace with the path to your image

# HTML body with embedded image
BODY_HTML = """
<!DOCTYPE html>
<html>
<body>
    <p>Dear {store_owner_name}</p>
    <p>We would love to see you at the upcoming Dallas Market Week, March 25th-28th. Please see our two booth options! Please email us directly if you would like to setup an appointment or linesheets</p>
    <br>
    <img src="cid:image1" alt="Embedded Image" style="width:100%; max-width:600px;">
    <p>Regards,<br>
       Ram Narayanan<br>
       CEO and Owner<br>
       Prince Peter Collection.</p>
</body>
</html>
"""

def send_email(recipient_email, subject, body_html, image_path,store_owner_name):
    body_html=body_html.format(store_owner_name=store_owner_name)
    """Function to send email using SMTP with an embedded image."""
    try:
        # Set up MIME
        msg = MIMEMultipart("related")
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach the HTML body
        msg_alternative = MIMEMultipart("alternative")
        msg.attach(msg_alternative)
        msg_alternative.attach(MIMEText(body_html, 'html'))

        # Attach the image
        with open(image_path, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-ID', '<image1>')  # Content ID used in HTML
            msg.attach(img)

        # Connect to Gmail SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())

        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")


def main():
    input_file = "scripts/assets/data_email_atl_v2.xlsx"  # Ensure the file path is correct
    df = pd.read_excel(input_file)

    for index, row in df.iterrows():
        # Safely extract and handle the name
        name = row['Name']
        if pd.isna(name) or isinstance(name, float):
            name = ""  # Convert NaN or float to empty string

        store_name = row['Store Name']  # Extract the store name

        # Determine the appropriate salutation
        if name.strip().lower() == "buyer" or not name.strip():
            store_owner_name = store_name  # Use store name if 'Name' is empty or says "Buyer"
        else:
            store_owner_name = name.strip()  # Use the name directly if it's valid

        emails = row['email'].split(',')  # Assuming the emails are in the 'email' column

        for email in emails:
            email = email.strip()
            if email:
                send_email(email, SUBJECT, BODY_HTML, IMAGE_PATH, store_owner_name)
                time.sleep(2)  # Delay to prevent rate-limiting

    print("All emails have been sent.")



if __name__ == "__main__":
    main()
