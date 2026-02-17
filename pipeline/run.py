from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "email_rules.json"
MOCK_EMAILS_PATH = ROOT / "data" / "mock_emails.json"
REPORT_PATH = ROOT / "reports" / "Daily_Productivity_Report.txt"

DATE_PATTERNS = [
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
    re.compile(r"\b[A-Za-z]{3,9}\s+\d{1,2},\s*\d{4}\b"),
    re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\b"),
]


@dataclass
class Email:
    sender: str
    subject: str
    body: str
    folder: str


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        config = json.load(file)

    config.setdefault("trusted_senders", [])
    config.setdefault("priority_keywords", [])
    config.setdefault("mode", "balanced")
    return config


def load_mock_emails(path: Path = MOCK_EMAILS_PATH) -> list[Email]:
    with path.open("r", encoding="utf-8") as file:
        items = json.load(file)
    return [Email(**item) for item in items]


def ai_summary_placeholder(email: Email) -> str:
    """Placeholder AI summary function for future LLM integration."""
    snippet = " ".join(email.body.split())
    if len(snippet) > 120:
        snippet = f"{snippet[:120]}..."
    return f"[AI-SUMMARY-PLACEHOLDER] {email.subject}: {snippet}"


def detect_deadlines_stub(email: Email) -> list[str]:
    """Deadline detection stub using simple date-pattern matching."""
    text = f"{email.subject}\n{email.body}"
    results: list[str] = []
    for pattern in DATE_PATTERNS:
        results.extend(pattern.findall(text))
    return list(dict.fromkeys(results))


def is_important_by_rule(email: Email, config: dict[str, Any]) -> tuple[bool, str]:
    trusted = {sender.strip().lower() for sender in config["trusted_senders"]}
    if email.sender.strip().lower() in trusted:
        return True, "trusted_sender"

    text = f"{email.subject} {email.body}".lower()
    for keyword in config["priority_keywords"]:
        if keyword.lower() in text:
            return True, f"keyword:{keyword}"

    return False, "none"


def process_emails(config: dict[str, Any], emails: list[Email]) -> dict[str, Any]:
    metrics = {
        "inbox_scanned": 0,
        "spam_reviewed": 0,
        "spam_deleted": 0,
        "spam_recovered": 0,
        "important_flagged": 0,
        "deadlines_found": 0,
    }

    important_items: list[dict[str, Any]] = []

    for email in emails:
        is_important, reason = is_important_by_rule(email, config)

        if email.folder == "spam":
            metrics["spam_reviewed"] += 1
            if is_important:
                metrics["spam_recovered"] += 1
                important_items.append(
                    {
                        "email": email,
                        "reason": reason,
                        "summary": ai_summary_placeholder(email),
                    }
                )
            else:
                metrics["spam_deleted"] += 1
            continue

        metrics["inbox_scanned"] += 1
        if is_important:
            important_items.append(
                {
                    "email": email,
                    "reason": reason,
                    "summary": ai_summary_placeholder(email),
                }
            )

    deadline_items: list[tuple[Email, str]] = []
    for item in important_items:
        deadlines = detect_deadlines_stub(item["email"])
        for deadline in deadlines:
            deadline_items.append((item["email"], deadline))

    metrics["important_flagged"] = len(important_items)
    metrics["deadlines_found"] = len(deadline_items)

    return {
        "metrics": metrics,
        "important_items": important_items,
        "deadline_items": deadline_items,
    }


def write_report(result: dict[str, Any]) -> Path:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    metrics = result["metrics"]
    important_items = result["important_items"]
    deadline_items = result["deadline_items"]

    with REPORT_PATH.open("w", encoding="utf-8") as file:
        file.write(f"Date: {date.today().isoformat()}\n")
        file.write(f"Inbox scanned: {metrics['inbox_scanned']}\n")
        file.write(
            "Spam reviewed: "
            f"{metrics['spam_reviewed']} "
            f"(auto-deleted: {metrics['spam_deleted']}, recovered: {metrics['spam_recovered']})\n"
        )
        file.write(f"Important flagged: {metrics['important_flagged']}\n")
        file.write(f"Deadlines found: {metrics['deadlines_found']}\n\n")

        file.write("Important Email Summaries\n")
        if not important_items:
            file.write("- None\n")
        for item in important_items:
            email = item["email"]
            file.write(
                f"- {email.subject} | sender={email.sender} | reason={item['reason']}\n"
                f"  {item['summary']}\n"
            )

        file.write("\nDetected Deadlines (stub)\n")
        if not deadline_items:
            file.write("- None\n")
        for email, deadline in deadline_items:
            file.write(f"- {email.subject}: {deadline}\n")

    return REPORT_PATH


def run() -> dict[str, Any]:
    config = load_config()
    emails = load_mock_emails()
    result = process_emails(config, emails)
    report_path = write_report(result)
    import os

    summary_dir = ROOT / "Documents/AI_Email_Assistant"
    os.makedirs(summary_dir, exist_ok=True)
    summary_path = summary_dir / "Important_Mail_Summary.txt"

    with summary_path.open("w", encoding="utf-8") as f:
        for item in result["important_items"]:
            email = item["email"]
            summary = item.get("summary", "[AI-SUMMARY-PLACEHOLDER]")
            f.write(f"{email.subject} | sender={email.sender} | reason={item['reason']}\n")
            f.write(f"{summary}\n\n")

    print(f"Important email summary written to {summary_path}")
    return {"report": str(report_path.relative_to(ROOT)), "metrics": result["metrics"]}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
