import smtplib
import imghdr
from email.message import EmailMessage
import base64
from typing import List

def send_email(sender_email: str, receiver_email: str, subject: str, message: str,
               base64_images: List[str] = None, image_names: List[str] = None,
               sender_password: str = ''):
    """
    Send an email with HTML content and optional base64 encoded image attachments.

    Args:
    - sender_email (str): Sender's email address.
    - receiver_email (str): Recipient's email address.
    - subject (str): Subject of the email.
    - message (str): HTML content of the email.
    - base64_images (List[str]): List of base64 encoded images (default: None).
    - image_names (List[str]): List of filenames for the images (default: None).
    - sender_password (str): Sender's email account password (default: '').

    Returns:
    - None
    """
    if base64_images is None:
        base64_images = []
    if image_names is None:
        image_names = []

    # Create an EmailMessage object
    email = EmailMessage()
    email['Subject'] = subject
    email['From'] = sender_email
    email['To'] = receiver_email
    email.set_content(message, subtype='html')
    
    # Add base64 encoded images as attachments
    for base64_image, image_name in zip(base64_images, image_names):
        image_data = base64.b64decode(base64_image)
        image_type = imghdr.what(None, h=image_data)  # Determine image file type
        email.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

    try:
        # Connect to SMTP server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, sender_password)
            smtp.send_message(email)
            print("Email sent successfully!")
            return True
    except smtplib.SMTPException as e:
        print("Unable to send email:", e)
        return False