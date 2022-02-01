from flask_mail import Message 
from flask import current_app 

from .. import Mail as mail

# Define send method 
def send_email(to, subject, template):
    msg = Message(
        subject=subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)