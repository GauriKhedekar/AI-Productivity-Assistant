from logging import config
import os
from pathlib import Path
import json
import re
from datetime import date
from typing import Any
import imaplib
import email as py_email
from email.header import decode_header
from pipeline.downloads_cleanup import cleanup_downloads
from pipeline.ai_summary import generate_daily_summary
from pipeline.calendar_integration import GoogleCalendarIntegration
from pipeline.spam_processor import process_spam_folder
from pipeline.email_utils import Email, extract_body, is_important_by_rule
from pipeline.user_setup import collect_user_preferences

import tkinter as tk
from tkinter import simpledialog  # <-- added for user input

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "email_rules.json"
CRED_PATH = ROOT / "config" / "email_credentials.json"
REPORT_PATH = ROOT / "reports/Daily_Productivity_Report.txt"

# -----------------------------
# Existing functions (unchanged)
# -----------------------------
def _extract_attachments(msg) -> list[dict[str, Any]]:
    attachments = []
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        filename = part.get_filename()
        if not filename:
            continue
        if isinstance(filename, str):
            try:
                filename = filename.encode('utf-8').decode('utf-8')
            except:
                pass
        content = part.get_payload(decode=True)
        content_type = part.get_content_type()
        attachments.append({
            'filename': filename,
            'content': content,
            'content_type': content_type,
        })
    return attachments

def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        config = json.load(f)
    config.setdefault("trusted_senders", [])
    config.setdefault("priority_keywords", [])
    return config

# -----------------------------
# Main run function
# -----------------------------
def run() -> dict[str, Any]:
    # ✅ Collect user preferences (credentials only once, rules every run)
    config = collect_user_preferences()

    # --- Load credentials & config ---
    with CRED_PATH.open("r", encoding="utf-8") as f:
        creds = json.load(f)
    config = load_config(CONFIG_PATH)

    print("Connecting...")
    server = imaplib.IMAP4_SSL(creds["imap_server"], creds["imap_port"])
    server.login(creds["email"], creds["password"])
    print("Connected.")

    # Step 1: Handle SPAM folder
    spam_metrics = process_spam_folder(server, use_alerts=True)
    metrics = {
        "spam_reviewed": spam_metrics.get("reviewed", 0),
        "spam_deleted": spam_metrics.get("deleted", 0),
        "spam_recovered": spam_metrics.get("recovered", 0),
    }
    print("Spam folder processing done.")
        
    # Fetch Inbox emails
    server.select("INBOX")
    status, messages = server.search(None, "ALL")
    inbox_mails = []
    important_items = []

    if status == "OK":
        mail_ids = messages[0].split()[-10:]
        for uid in mail_ids:
            typ, msg_data = server.fetch(uid, "(RFC822)")
            if typ != "OK":
                continue
            msg = py_email.message_from_bytes(msg_data[0][1])

            subject = ""
            if msg["Subject"]:
                for part, enc in decode_header(msg["Subject"]):
                    if isinstance(part, bytes):
                        subject += part.decode(enc or "utf-8", errors="ignore")
                    else:
                        subject += part

            sender = msg.get("From", "")
            body = extract_body(msg)
            email_obj = Email(sender=sender, subject=subject, body=body, folder="INBOX")
            inbox_mails.append(email_obj)


            is_important, _ = is_important_by_rule(email_obj, config)
            if is_important:
                important_items.append(email_obj)

    # GOOGLE CALENDAR INTEGRATION
    calendar_client = GoogleCalendarIntegration()
    success, msg = calendar_client.authenticate()
    print(f"Google Calendar: {msg}")

    calendar_metrics = {"events_created": 0, "errors": 0}
    for email_obj in important_items:
        try:
            title = (email_obj.subject or email_obj.body or "Email Event")[:70]
            description = title
        
            success, event_id, event_link_or_msg = calendar_client.create_event(title=title, description=description)

            if success:
                calendar_metrics['events_created'] += 1
                print(f"✓ Calendar event created: {title}")
                print(f"  View event: {event_link_or_msg}")
            else:
                calendar_metrics['errors'] += 1
                print(f"✗ Failed to create event: {event_link_or_msg}")

        except Exception as e:
              calendar_metrics['errors'] += 1
              print(f"Calendar error: {e}")

    # DOWNLOADS CLEANUP
    files_organized = cleanup_downloads()
    print(f"Files organized from Downloads: {files_organized}")

    # Update metrics
    metrics.update({
        "inbox_scanned": len(inbox_mails),
        "important_flagged": len(important_items),
        "files_organized": files_organized,
        "calendar_events_created": calendar_metrics['events_created'],
        "calendar_errors": calendar_metrics['errors'],
    })

    # Prepare AI summary
    structured_emails = []
    for e in important_items:
        subj = (e.subject or "").strip()
        body = (e.body or "").strip().replace("\n", " ")
        if subj and subj.lower() not in ["no subject", ""]:
            structured_emails.append(subj[:200])
        elif body:
            structured_emails.append(body[:200])
        else:
            structured_emails.append(f"Email from {e.sender}")

    if structured_emails:
        summary_prompt_data = f"""
You are an executive productivity assistant.
Generate a DAILY EMAIL SUMMARY for {len(important_items)} emails.
STRICT OUTPUT RULES (MUST FOLLOW):
- Use ONLY numbered bullets starting with "1.", "2.", "3."
- One numbered point per email
- Maximum 2 short sentences per bullet
- Insert EXACTLY one blank line after each numbered point
- Do NOT add headings like CONTEXT, ACTION ITEMS, or ID
- Do NOT add raw URLs
- Do NOT repeat sender or subject labels
- Do NOT invent information
- Ignore marketing language and promotional fluff
- Focus on meaningful updates, requests, or "deadlines"
- All important emails summary must be included as per number of important emails.

Emails:
{chr(10).join(structured_emails)}
"""
        ai_summary = generate_daily_summary(summary_prompt_data)
    else:
        ai_summary = "No important emails detected today."

    # WRITE REPORT
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write(f"Date: {date.today().isoformat()}\n")
        f.write(f"Inbox scanned: {metrics['inbox_scanned']}\n")
        f.write(
            f"Files organized from Downloads: {metrics['files_organized']}\n"
            f"Spam reviewed: {metrics['spam_reviewed']}\n"
            f"Spam deleted: {metrics['spam_deleted']}\n"
            f"Spam recovered: {metrics['spam_recovered']}\n"
            f"Calendar events created: {metrics['calendar_events_created']}\n\n"
        )
        f.write(f"Important flagged: {metrics['important_flagged']}\n")
        f.write("====== AI SUMMARY ======\n")
        f.write(ai_summary)

    return {"report": str(REPORT_PATH.relative_to(ROOT)), "metrics": metrics}

if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2))
