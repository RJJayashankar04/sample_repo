from __future__ import annotations

import getpass
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("BOSCH_SMTP_SERVER", "")
SMTP_PORT = int(os.getenv("BOSCH_SMTP_PORT", ""))
SENDER_EMAIL = os.getenv("BOSCH_SENDER_EMAIL", "")


def send_outlook_email(
    recipient: str,
    subject: str,
    text: str,
    html: str | None = None,
) -> None:
    if not SMTP_SERVER or not SENDER_EMAIL:
        raise RuntimeError(
            "Set SMTP_SERVER and SENDER_EMAIL in your environment or .env file."
        )

    password = os.getenv("PASSWORD")
    if not password:
        password = getpass.getpass("Email account password: ")

    message = EmailMessage()
    message["From"] = SENDER_EMAIL
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(text)

    if html:
        message.add_alternative(html, subtype="html")

    tls_context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15) as server:
        server.ehlo()
        server.starttls(context=tls_context)
        server.ehlo()
        server.login(SENDER_EMAIL, password)
        server.send_message(message)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('Usage: python mail_test.py RECIPIENT "SUBJECT" "MESSAGE"')
        raise SystemExit(1)

    send_outlook_email(
        recipient=sys.argv[1],
        subject=sys.argv[2],
        text=sys.argv[3],
    )
