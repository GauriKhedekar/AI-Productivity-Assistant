# AI Productivity Email Intelligence System

A minimal, config-driven MVP that processes mock emails and generates a daily productivity report.

## Overview

This project demonstrates a **rule-first email triage pipeline** with AI-ready extension points:

- Loads email rules from `config/email_rules.json`
- Ingests mock emails from `data/mock_emails.json`
- Classifies emails using deterministic rules:
  - trusted sender match
  - priority keyword match
- Applies spam-folder handling (auto-delete vs recover)
- Runs a deadline-detection stub (regex-based date matching)
- Uses an AI summary placeholder for important messages
- Writes `reports/Daily_Productivity_Report.txt`

## Current MVP Architecture

```text
Mock Email Source (JSON)
  ↓
Config Loading
  ↓
Rule Engine (trusted_senders + priority_keywords)
  ↓
Spam Handling + Important Mail Flagging
  ↓
Deadline Detection Stub (regex patterns)
  ↓
Report Writer
  ↓
reports/Daily_Productivity_Report.txt
```

## Repository Structure

```text
AI-Productivity-Assistant/
├── config/
│   └── email_rules.json
├── data/
│   ├── mock_emails.json
│   └── mock_downloads/
├── pipeline/
│   ├── __init__.py
│   └── run.py
├── reports/
│   ├── Daily_Productivity_Report.txt
│   ├── Day-3-Report.md
│   └── Day-3-Report-Template.md
└── tests/
    ├── conftest.py
    └── test_run.py
```

## Configuration

Edit `config/email_rules.json`:

- `trusted_senders`: senders always treated as important
- `priority_keywords`: keywords that mark emails as important
- `mode`: reserved field for future behavior modes

## How to Run

From the repository root:

```bash
python pipeline/run.py
```

Expected output:

- Console JSON summary with report path + metrics
- Generated file: `reports/Daily_Productivity_Report.txt`

## Testing

Run unit tests with:

```bash
pytest -q
```

Test coverage includes:

- config loading defaults
- rule-based classification behavior
- report file generation

## Next Steps After MVP

- Integrate real email providers (IMAP/Gmail API)
- Replace summary placeholder with LLM-based summarization/classification
- Improve deadline detection with date normalization and timezone handling
- Add calendar-event creation and reminder stubs
- Add downloads cleanup pipeline and routing rules
- Expand tests for deadline extraction edge cases and end-to-end runs
