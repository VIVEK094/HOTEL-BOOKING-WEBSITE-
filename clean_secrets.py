#!/usr/bin/env python3
import sys
import re

def clean_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Remove lines with secrets
    content = re.sub(r"STRIPE_SECRET_KEY = '.*'\n", "", content)
    content = re.sub(r"TWILIO_ACCOUNT_SID = '.*'\n", "", content)
    content = re.sub(r"TWILIO_AUTH_TOKEN = '.*'\n", "", content)
    content = re.sub(r"EMAIL_HOST_PASSWORD = '.*'\n", "", content)
    content = re.sub(r"PAYPAL_CLIENT_SECRET = '.*'\n", "", content)
    content = re.sub(r"STRIPE_PUBLIC_KEY = '.*'\n", "", content)
    content = re.sub(r"PAYPAL_CLIENT_ID = '.*'\n", "", content)
    content = re.sub(r"TWILIO_WHATSAPP_NUMBER = '.*'\n", "", content)
    content = re.sub(r"EMAIL_HOST_USER = '.*'\n", "", content)
    content = re.sub(r"DEFAULT_FROM_EMAIL = '.*'\n", "", content)

    with open(filename, 'w') as f:
        f.write(content)

if __name__ == '__main__':
    clean_file('hotel/settings.py')
