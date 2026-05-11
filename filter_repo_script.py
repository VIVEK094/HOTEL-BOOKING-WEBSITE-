#!/usr/bin/env python3
import sys
import re

def blob_callback(blob):
    if blob.filename == b'hotel/settings.py':
        content = blob.data.decode('utf-8')
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
        blob.data = content.encode('utf-8')
    return blob

if __name__ == '__main__':
    import git_filter_repo as fr
    fr.RepoFilter(blob_callback=blob_callback).run()
