# pipeline/user_setup.py
import json
import tkinter as tk
from tkinter import simpledialog, messagebox
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "email_rules.json"

def load_config():
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {
            "email": "",
            "app_password": "",
            "trusted_senders": [],
            "priority_keywords": []
        }
    return data

def save_config(data):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def collect_user_preferences():
    root = tk.Tk()
    root.withdraw()

    data = load_config()

    # ---- ASK CREDENTIALS ONLY IF NOT PRESENT ----
    if not data.get("email"):
        data["email"] = simpledialog.askstring("Gmail Login", "Enter Gmail address:")

    if not data.get("app_password"):
        data["app_password"] = simpledialog.askstring(
            "Gmail App Password",
            "Enter 16-digit Gmail App Password:",
            show="*"
        )

    # ---- ALWAYS ASK FOR NEW KEYWORDS (EVERY RUN) ----
    new_keywords = []
    while True:
        keyword = simpledialog.askstring(
            "Important Keyword",
            "Add important keyword (Cancel to finish):"
        )
        if not keyword:
            break
        if keyword not in data["priority_keywords"]:
            data["priority_keywords"].append(keyword)
            new_keywords.append(keyword)

    # ---- ALWAYS ASK FOR NEW TRUSTED SENDERS ----
    new_senders = []
    while True:
        sender = simpledialog.askstring(
            "Trusted Sender",
            "Add trusted sender email (Cancel to finish):"
        )
        if not sender:
            break
        if sender not in data["trusted_senders"]:
            data["trusted_senders"].append(sender)
            new_senders.append(sender)

    save_config(data)

    messagebox.showinfo(
        "Preferences Updated",
        f"Added {len(new_keywords)} keywords and {len(new_senders)} trusted senders."
    )

    root.destroy()
    return data
