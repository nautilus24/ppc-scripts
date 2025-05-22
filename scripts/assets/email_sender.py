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
IMAGE_PATH = "C:/Users/priya/Downloads/Merged_document.jpg"  # Replace with the path to your image

# HTML body with embedded image
BODY_HTML = """
<!DOCTYPE html>
<html>
<body>
    <p>Dear Buyers:</p>
    <p>Our brand is Prince Peter Collection. We create licensed and generic graphic tees all made in the United States. We are running a promotion for the upcoming January 2025 Dallas Market Week!</p>
    <br>
    <p>We are offering all our tees at $16.00 a unit. We are offer licensed band tees for $16.00 a unit! We are offering all our pullovers at $22.00 a unit! We have a 6 unit per style minimum, and a $500 minimum order. Please come and see us! We would love to show you our 200+ styles in stock!</p>
    <img src="cid:image1" alt="Embedded Image" style="width:100%; max-width:600px;">
    <p>Regards,<br>
       Ram Narayanan<br>
       CEO and Owner<br>
       Prince Peter Collection.</p>
</body>
</html>
"""

def send_email(recipient_email, subject, body_html, image_path):
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
    # Load the input file
    input_file = "scripts/assets/data_email_test.xlsx"  # Replace with your file name
    df = pd.read_excel(input_file)

    # Iterate over each row
    for index, row in df.iterrows():
        emails = row['keyword'].split(',')  # Split multiple emails by commas

        for email in emails:
            email = email.strip()  # Clean any extra spaces
            if email:  # Ensure email is not empty
                send_email(email, SUBJECT, BODY_HTML, IMAGE_PATH)
                time.sleep(2)  # Optional: Add delay to prevent rate-limiting

    print("All emails have been sent.")

if __name__ == "__main__":
    main()
