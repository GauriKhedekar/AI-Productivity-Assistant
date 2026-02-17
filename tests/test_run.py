from pathlib import Path

from pipeline import run
from pipeline.run import Email


def test_load_config_applies_defaults(tmp_path: Path) -> None:
    config_file = tmp_path / "email_rules.json"
    config_file.write_text('{"trusted_senders": ["mentor@example.com"]}', encoding="utf-8")

    config = run.load_config(config_file)

    assert config["trusted_senders"] == ["mentor@example.com"]
    assert config["priority_keywords"] == []
    assert config["mode"] == "balanced"


def test_process_emails_classifies_mock_emails() -> None:
    config = {
        "trusted_senders": ["boss@company.com"],
        "priority_keywords": ["deadline", "assignment"],
        "mode": "balanced",
    }
    emails = [
        Email(
            sender="boss@company.com",
            subject="Status update",
            body="Please review this today.",
            folder="inbox",
        ),
        Email(
            sender="alerts@school.edu",
            subject="Assignment posted",
            body="New assignment available.",
            folder="inbox",
        ),
        Email(
            sender="promo@ads.com",
            subject="Buy now",
            body="Limited offer.",
            folder="spam",
        ),
    ]

    result = run.process_emails(config, emails)

    metrics = result["metrics"]
    assert metrics["inbox_scanned"] == 2
    assert metrics["spam_reviewed"] == 1
    assert metrics["spam_deleted"] == 1
    assert metrics["spam_recovered"] == 0
    assert metrics["important_flagged"] == 2

    reasons = [item["reason"] for item in result["important_items"]]
    assert "trusted_sender" in reasons
    assert "keyword:assignment" in reasons


def test_write_report_creates_file(tmp_path: Path, monkeypatch) -> None:
    report_path = tmp_path / "Daily_Productivity_Report.txt"
    monkeypatch.setattr(run, "REPORT_PATH", report_path)

    result = {
        "metrics": {
            "inbox_scanned": 2,
            "spam_reviewed": 1,
            "spam_deleted": 1,
            "spam_recovered": 0,
            "important_flagged": 1,
            "deadlines_found": 1,
        },
        "important_items": [
            {
                "email": Email(
                    sender="mentor@example.com",
                    subject="Assignment deadline",
                    body="Submit by 2026-02-20.",
                    folder="inbox",
                ),
                "reason": "keyword:assignment",
                "summary": "[AI-SUMMARY-PLACEHOLDER] Assignment deadline: Submit by 2026-02-20.",
            }
        ],
        "deadline_items": [
            (
                Email(
                    sender="mentor@example.com",
                    subject="Assignment deadline",
                    body="Submit by 2026-02-20.",
                    folder="inbox",
                ),
                "2026-02-20",
            )
        ],
    }

    generated = run.write_report(result)

    assert generated == report_path
    assert report_path.exists()
    content = report_path.read_text(encoding="utf-8")
    assert "Important Email Summaries" in content
    assert "Detected Deadlines (stub)" in content
    assert "Assignment deadline" in content
