import smtplib
from email.message import EmailMessage
from threading import Thread

from database import config


def send_mail_async(recipient: str, subject: str, content: str) -> None:
    t = Thread(target=send_mail, args=(recipient, subject, content))
    t.start()


def send_mail(recipient: str, subject: str, content: str) -> None:
    creds = config["mail_credentials"]

    server = smtplib.SMTP(creds["server"], creds["port"])
    server.starttls()

    server.login(creds["address"], creds["password"])

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = creds["address"]
    msg["To"] = recipient
    msg.set_content(content)

    server.send_message(msg)

    server.quit()
