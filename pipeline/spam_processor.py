"""
Spam Processor - Stable Final Version
(Trusted senders + rule-based importance + auto recovery)
"""

import os
import json
import email as py_email
from email.header import decode_header
from email.utils import parseaddr

from pipeline.email_utils import Email, extract_body, is_important_by_rule
from pipeline.learning_manager import LearningManager
from pipeline.alert_manager import AlertManager


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "email_rules.json")


def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠ Config load failed: {e}")
        return {
            "trusted_senders": [],
            "priority_keywords": [],
            "mode": "balanced"
        }


# =========================================================
# IMPORTANCE LOGIC
# =========================================================

def _determine_importance(email_obj: Email, config: dict, learning_manager: LearningManager):
    """
    Returns:
        "trusted" → sender is trusted
        "rule" → matched rule-based importance
        None → not important
    """

    sender = email_obj.sender.lower()

    # ✅ Trusted sender (auto recover, no alert)
    if learning_manager.is_trusted_sender(sender):
        return "trusted"

    # ✅ Rule-based importance
    is_important, _ = is_important_by_rule(email_obj, config)
    if is_important:
        return "rule"

    return None


# =========================================================
# MAIN SPAM PROCESSING
# =========================================================

def process_spam_folder(server, use_alerts: bool = True):

    config = load_config()
    learning_manager = LearningManager()
    alert_manager = AlertManager(use_gui=use_alerts)

    metrics = {
        "reviewed": 0,
        "recovered": 0,
        "deleted": 0,
        "learned_important": 0,
        "recovered_senders": []
    }

    try:
        spam_folders = ["[Gmail]/Spam", "Spam"]

        folder_selected = False
        for folder in spam_folders:
            status, _ = server.select(folder)
            if status == "OK":
                folder_selected = True
                break

        if not folder_selected:
            print("❌ Could not select Spam folder.")
            return metrics

        status, messages = server.search(None, "ALL")
        if status != "OK":
            return metrics

        mail_ids = messages[0].split()

        if not mail_ids:
            return metrics

        mail_ids = mail_ids[-20:]

        for uid in mail_ids:
            metrics["reviewed"] += 1

            typ, msg_data = server.fetch(uid, "(RFC822)")
            if typ != "OK":
                continue

            msg = py_email.message_from_bytes(msg_data[0][1])

            subject = ""
            if msg.get("Subject"):
                for part, enc in decode_header(msg["Subject"]):
                    if isinstance(part, bytes):
                        subject += part.decode(enc or "utf-8", errors="ignore")
                    else:
                        subject += part

            raw_sender = msg.get("From", "")
            _, email_address = parseaddr(raw_sender)
            sender = email_address.strip().lower()

            body = extract_body(msg)

            email_obj = Email(
                sender=sender,
                subject=subject,
                body=body,
                folder="SPAM"
            )

            importance_type = _determine_importance(
                email_obj,
                config,
                learning_manager
            )

            move_to_inbox = False

            # ===============================
            # TRUSTED → auto recover (NO alert)
            # ===============================
            if importance_type == "trusted":
                move_to_inbox = True

            # ===============================
            # RULE-BASED → ask user (if alerts enabled)
            # ===============================
            elif importance_type == "rule":
                if use_alerts:
                    move_to_inbox, _ = alert_manager.show_email_alert(
                        sender=sender,
                        subject=subject,
                        preview=body[:300]
                    )
                else:
                    move_to_inbox = True

            # ===============================
            # MOVE IMPORTANT EMAILS
            # ===============================
            if move_to_inbox:
                try:
                    server.copy(uid, "INBOX")
                    server.store(uid, "+FLAGS", "\\Deleted")

                    learning_manager.add_trusted_sender(sender)

                    metrics["recovered"] += 1
                    metrics["learned_important"] += 1
                    metrics["recovered_senders"].append(sender)

                    print(f"✓ Recovered → {subject} ({sender})")

                except Exception as e:
                    print(f"✗ Recovery failed: {e}")

            else:
                try:
                    server.store(uid, "+FLAGS", "\\Deleted")
                    metrics["deleted"] += 1
                except Exception as e:
                    print(f"✗ Delete failed: {e}")

        server.expunge()

    except Exception as e:
        print(f"❌ Spam processing error: {e}")

    return metrics
