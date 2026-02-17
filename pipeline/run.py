from __future__ import annotations

import json
import logging
import re
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "email_rules.json"
MOCK_EMAILS_PATH = ROOT / "data" / "mock_emails.json"
REPORTS_DIR = ROOT / "reports"
LOGS_DIR = ROOT / "logs"
DOWNLOADS_DIR = ROOT / "data" / "mock_downloads"

DATE_PATTERNS = [
    re.compile(r"\b(\d{4}-\d{2}-\d{2})\b"),
    re.compile(r"\b([A-Za-z]{3,9}\s+\d{1,2},\s*\d{4})\b"),
    re.compile(r"\b(\d{1,2}/\d{1,2}/\d{4})\b"),
]


@dataclass
class Email:
    sender: str
    subject: str
    body: str
    folder: str


@dataclass
class ClassificationResult:
    label: str
    confidence: float
    summary: str


class AIRouter:
    """Stub AI layer for local deterministic classification and summaries."""

    IMPORTANT_HINTS = (
        "interview",
        "deadline",
        "assignment",
        "submit",
        "registration",
        "internship",
        "meeting",
        "offer",
        "project",
        "hackathon",
    )

    def classify_importance(self, email: Email) -> ClassificationResult:
        text = f"{email.subject} {email.body}".lower()
        score = sum(1 for hint in self.IMPORTANT_HINTS if hint in text)
        if score >= 2:
            label, confidence = "important", 0.88
        elif score == 1:
            label, confidence = "important", 0.72
        else:
            label, confidence = "not_important", 0.81
        return ClassificationResult(
            label=label,
            confidence=confidence,
            summary=self.summarize(email),
        )

    def classify_spam(self, email: Email) -> ClassificationResult:
        text = f"{email.subject} {email.body}".lower()
        spam_words = ("win", "lottery", "bitcoin", "urgent offer", "click now", "free")
        score = sum(1 for word in spam_words if word in text)
        if score >= 2:
            return ClassificationResult("spam", 0.95, "Likely promotional spam.")
        if score == 1:
            return ClassificationResult("review", 0.65, "Possibly spam; review suggested.")
        return ClassificationResult("important", 0.56, "Does not match common spam markers.")

    def summarize(self, email: Email) -> str:
        compact = re.sub(r"\s+", " ", email.body).strip()
        short = compact[:220] + ("..." if len(compact) > 220 else "")
        return f"{email.subject}: {short}"


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        config = json.load(f)
    config.setdefault("trusted_senders", [])
    config.setdefault("priority_keywords", [])
    config.setdefault("mode", "balanced")
    return config


def load_mock_emails(path: Path = MOCK_EMAILS_PATH) -> list[Email]:
    with path.open("r", encoding="utf-8") as f:
        rows = json.load(f)
    return [Email(**row) for row in rows]


def setup_logging() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(LOGS_DIR / "pipeline.log"), logging.StreamHandler()],
    )


def is_priority_by_rule(email: Email, config: dict[str, Any]) -> tuple[bool, str]:
    sender = email.sender.lower().strip()
    trusted = {s.lower().strip() for s in config["trusted_senders"]}
    if sender in trusted:
        return True, "trusted_sender"

    text = f"{email.subject} {email.body}".lower()
    for kw in config["priority_keywords"]:
        if kw.lower() in text:
            return True, f"keyword:{kw}"

    return False, "none"


def extract_deadlines(email: Email) -> list[str]:
    text = f"{email.subject}\n{email.body}"
    found: list[str] = []
    for pattern in DATE_PATTERNS:
        found.extend(pattern.findall(text))
    seen: set[str] = set()
    deduped: list[str] = []
    for item in found:
        if item not in seen:
            seen.add(item)
            deduped.append(item)
    return deduped


def organize_downloads(downloads_dir: Path = DOWNLOADS_DIR) -> dict[str, int]:
    downloads_dir.mkdir(parents=True, exist_ok=True)
    category_map = {
        "resume": "Resume",
        "cv": "Resume",
        "certificate": "Certificates",
        "project": "Projects",
        "assignment": "College",
        "college": "College",
    }

    moved = 0
    per_category: Counter[str] = Counter()

    for item in downloads_dir.iterdir():
        if item.is_dir():
            continue

        lower = item.name.lower()
        target_cat = "Others"
        for token, category in category_map.items():
            if token in lower:
                target_cat = category
                break

        target_dir = downloads_dir / target_cat
        target_dir.mkdir(exist_ok=True)
        item.rename(target_dir / item.name)
        moved += 1
        per_category[target_cat] += 1

    result = {"total_moved": moved}
    result.update(dict(per_category))
    return result


def run_pipeline() -> dict[str, Any]:
    setup_logging()
    config = load_config()
    emails = load_mock_emails()
    ai = AIRouter()

    metrics = {
        "inbox_scanned": 0,
        "spam_reviewed": 0,
        "spam_deleted": 0,
        "spam_recovered": 0,
        "spam_review_bucket": 0,
        "important_flagged": 0,
        "deadlines_found": 0,
    }

    important_items: list[dict[str, Any]] = []

    for email in emails:
        if email.folder == "spam":
            metrics["spam_reviewed"] += 1
            by_rule, reason = is_priority_by_rule(email, config)
            if by_rule:
                metrics["spam_recovered"] += 1
                summary = ai.summarize(email)
                important_items.append({"email": email, "reason": reason, "summary": summary})
                logging.info("Recovered spam mail by rule: %s", email.subject)
                continue

            ai_result = ai.classify_spam(email)
            if ai_result.label == "spam" and ai_result.confidence >= 0.9:
                metrics["spam_deleted"] += 1
            elif ai_result.label == "important":
                metrics["spam_recovered"] += 1
                important_items.append({"email": email, "reason": "ai_spam_recovery", "summary": ai_result.summary})
            else:
                metrics["spam_review_bucket"] += 1
            continue

        metrics["inbox_scanned"] += 1
        by_rule, reason = is_priority_by_rule(email, config)
        if by_rule:
            important_items.append({"email": email, "reason": reason, "summary": ai.summarize(email)})
            continue

        ai_result = ai.classify_importance(email)
        if ai_result.label == "important" and ai_result.confidence >= 0.7:
            important_items.append({"email": email, "reason": "ai_importance", "summary": ai_result.summary})

    deadline_entries: list[tuple[Email, str]] = []
    for item in important_items:
        email = item["email"]
        deadlines = extract_deadlines(email)
        for d in deadlines:
            deadline_entries.append((email, d))

    metrics["important_flagged"] = len(important_items)
    metrics["deadlines_found"] = len(deadline_entries)

    summary_path = REPORTS_DIR / "Important_Mail_Summary.txt"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with summary_path.open("w", encoding="utf-8") as f:
        for item in important_items:
            email = item["email"]
            matching_deadlines = [d for e, d in deadline_entries if e is email]
            f.write(
                f"Sender: {email.sender}\n"
                f"Subject: {email.subject}\n"
                f"Reason: {item['reason']}\n"
                f"Summary: {item['summary']}\n"
                f"Detected deadline: {', '.join(matching_deadlines) if matching_deadlines else 'None'}\n"
                "---\n"
            )

    download_metrics = organize_downloads()

    report_date = date.today().isoformat()
    report_path = REPORTS_DIR / f"Daily_Productivity_Report_{report_date}.md"
    with report_path.open("w", encoding="utf-8") as f:
        f.write(
            f"Date: {report_date}\n"
            f"Inbox scanned: {metrics['inbox_scanned']}\n"
            f"Spam reviewed: {metrics['spam_reviewed']} (auto-deleted: {metrics['spam_deleted']}, kept/recovered: {metrics['spam_recovered']}, review: {metrics['spam_review_bucket']})\n"
            f"Important flagged: {metrics['important_flagged']}\n"
            f"Deadlines found: {metrics['deadlines_found']}\n"
            f"Downloads organized: {download_metrics['total_moved']} files\n\n"
            "Highlights\n"
        )
        for item in important_items[:5]:
            email = item["email"]
            f.write(f"- {email.subject} ({item['reason']})\n")

        f.write("\nAction Items\n")
        if deadline_entries:
            for email, d in deadline_entries[:8]:
                f.write(f"- {email.subject}: due {d}\n")
        else:
            f.write("- No explicit deadlines detected today.\n")

    logging.info("Pipeline completed. Report: %s", report_path)
    return {
        "report_path": str(report_path.relative_to(ROOT)),
        "summary_path": str(summary_path.relative_to(ROOT)),
        "metrics": metrics,
        "download_metrics": download_metrics,
    }


if __name__ == "__main__":
    result = run_pipeline()
    print(json.dumps(result, indent=2))
