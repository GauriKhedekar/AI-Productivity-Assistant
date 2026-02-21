import re
from dataclasses import dataclass
from email.utils import parseaddr


@dataclass
class Email:
    sender: str
    subject: str
    body: str
    folder: str


def extract_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode(errors="ignore").strip()

            if content_type == "text/html" and "attachment" not in content_disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    html = payload.decode(errors="ignore")
                    return re.sub("<.*?>", "", html).strip()
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            return payload.decode(errors="ignore").strip()

    return ""

def is_important_by_rule(email_obj: Email, config):
    _, sender_email = parseaddr(email_obj.sender)
    sender_email = sender_email.lower().strip()

    trusted = {s.lower().strip() for s in config.get("trusted_senders", [])}
    keywords = [k.lower() for k in config.get("priority_keywords", [])]

    # Trusted sender → always important
    if sender_email in trusted:
        return True, "trusted_sender"

    # Keyword detection
    text = f"{email_obj.subject} {email_obj.body}".lower()
    for keyword in keywords:
        if keyword in text:
            return True, f"keyword:{keyword}"

    return False, "none"
