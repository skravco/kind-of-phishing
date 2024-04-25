import smtplib
from email.mime.text import MIMEText

import os


def intercept_msg(customer, email, phone, dealer, rating, comments):
    port = 2525
    smtp_server = "smtp.mailtrap.io"
    login = os.environ.get("MAILTRAP_LOGIN")   
    password = os.environ.get("MAILTRAP_PASSWD")  
    message = f"<h3>New Submission</h3><ul><li>Customer: {customer}</li><li>Email: {email}</li><li>Phone: {phone}</li><li>Provider: {dealer}</li><li>Severity: {rating}</li><li>Comments: {comments}</li></ul>"

    sender = f"{email}"
    receiver = "noreply@trap.com"
    msg = MIMEText(message, "html")
    msg["Subject"] = "KindOfAnotherPhishingAttemp"
    msg["From"] = sender
    msg["To"] = receiver

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender, receiver, msg.as_string())
