# AI Productivity Email Intelligence System

A config-driven, hybrid AI + rule-based productivity assistant that automates email triage, deadline extraction, downloads cleanup, and daily reporting.

## What this project does

- Classifies emails as spam/important using:
  - deterministic rules (`trusted_senders`, `priority_keywords`)
  - AI-style fallback classification for uncertain cases (local deterministic stub)
- Generates summaries for important emails
- Extracts date-like deadlines from important emails
- Organizes files in a downloads folder into categories
- Produces a daily productivity report and logs

## Architecture

```text
Email Sources (mock/local)
  ↓
Ingestion
  ↓
Rule Engine (trusted senders + keywords)
  ↓
AI Classification (uncertain/priority)
  ↓
Deadline Extraction
  ↓
Downloads Cleanup
  ↓
Daily Report + Summary + Logs
```

## Project structure

```text
AI-Productivity-Assistant/
├── config/
│   └── email_rules.json
├── data/
│   ├── mock_emails.json
│   └── mock_downloads/
├── docs/
│   └── project_design.md
├── logs/
├── pipeline/
│   ├── __init__.py
│   └── run.py
└── reports/
```

## Configuration

Edit `config/email_rules.json`:

- `trusted_senders`: always considered important
- `priority_keywords`: rule-based important markers
- `mode`: strategy preset placeholder

## Run

```bash
python pipeline/run.py
```

Outputs:

- `reports/Daily_Productivity_Report_<YYYY-MM-DD>.md`
- `reports/Important_Mail_Summary.txt`
- `logs/pipeline.log`

## Current status

This repository now includes an end-to-end MVP pipeline with mock data and deterministic AI stubs.

Planned next steps:
- Real email provider integration (Gmail/IMAP)
- LLM-backed summarization/classification
- Calendar API integration
- Rich UI dashboard
