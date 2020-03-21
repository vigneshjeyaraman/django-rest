import sendgrid
import json
import ssl
from sendgrid.helpers.mail import Mail, Email, Content, To
from config.local import SEND_GRID_API_KEY, FROM_EMAIL
def send_email(email, otp):
    """
        send_email function used to send email.
    :param email:
    :param path:
    :return: True
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    send_grid = sendgrid.SendGridAPIClient(api_key=SEND_GRID_API_KEY)
    from_email = Email(FROM_EMAIL)
    to_email = To(email=email)
    subject = 'forgot password'
    content = Content("text/plain", otp)
    mail = Mail(from_email, to_email, subject, content)
    send_grid.send(mail)
    return True