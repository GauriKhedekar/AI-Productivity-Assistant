# AI Productivity Email Intelligence System

## Table of Contents


- Project Overview
- 📌 Problem Statement
- 🚀 Features
- Project Status
- Key Modules
- 🧠 Architecture Overview
- 📂 Folder Structure
- Setup Instructions
- Configuration
- Outputs & Storage
- Usage
- 🛠 Tech Stack
- Why This Is Different
- Roadmap
- Contributing
- License
- Demo

---

## Project Overview


**Problem statement:** Students and professionals struggle with spam overload, missed important emails, forgotten deadlines, unorganized downloads, and no daily productivity tracking.  
**Target users:** Students, interns, and professionals managing high-volume email.  
**Core value proposition:** Automates inbox triage and daily reporting so users stay focused and never miss critical updates.  
**Key features:** Spam intelligence, Important mail detection, Deadline extraction, Download cleanup, Daily reporting.

---

## 📌 Problem Statement


Students and professionals struggle with:

- Spam overload  
- Missing important internship or assignment emails  
- Forgetting deadlines  
- Unorganized downloads  
- No daily productivity tracking  

This project builds an AI-powered automation system to solve these problems.

---

## 🚀 Features

### 1️⃣ Spam Intelligence


- Scan spam folder  
- Recover trusted emails  
- AI classify junk  
- Review uncertain mails  
- Clean trash safely  

### 2️⃣ Important Mail Intelligence


- Scan inbox  
- Detect internship, hackathon, assignment emails  
- Generate AI summary  

### 3️⃣ Deadline Detection


- Extract submission dates  
- Create calendar event  
- Add reminder  

### 4️⃣ Downloads Cleanup


- Organize files into folders  
- Smart rename files  

### 5️⃣ Daily Productivity Report


- Generate summary report  
- Track productivity metrics  

---

## Project Status


This project now includes a **minimal runnable pipeline (`pipeline/run.py`)** that generates a deterministic daily report using mock email data. The architecture is ready for integration with real email providers and AI APIs.  
All design and configuration docs are present; full implementation of AI classification, calendar integration, and downloads cleanup is planned.

---

## Key Modules


- **Spam Intelligence**: scan spam, apply trusted-sender/keyword rules, then AI classify uncertain cases.  
- **Important Mail Intelligence**: hybrid importance detection with summaries for all important emails.  
- **Deadline Extraction**: extract dates/titles from important emails and create calendar events (planned).  
- **Downloads Cleanup**: organize files into categorized folders and optionally rename (planned).  
- **Daily Reporting**: generate daily productivity metrics and summaries (planned).  
- **Learning Loop**: update trusted senders/keywords based on user feedback (planned).

---

## 🧠 Architecture Overview


```
High-level flow: Ingestion → Rule Engine → AI Classification → Deadline Detection → Report Generation → Storage

Email Sources
↓
Ingestion
↓
Rule Engine (config/email_rules.json)
↓
AI Classification (uncertain/priority)
↓
Deadline Detection
↓
Report Generation
↓
Storage (reports/, logs/)
```

Rule-based decisions handle known senders and explicit rules, while AI-based classification resolves uncertain or high-priority emails. Behavior is config-driven via `config/email_rules.json`.

---

## 📂 Folder Structure


```
AI-Productivity-Assistant/
├── config/ # Rule definitions (email_rules.json)
├── docs/ # Design notes
├── logs/ # Runtime logs (.gitkeep keeps empty dirs)
├── reports/ # Daily reports and summaries
└── README.md
```

---

## Setup Instructions


1. Clone the repository:  
   `git clone <repo-url>`  
2. Install dependencies (placeholder):  
   `pip install -r requirements.txt`  
   *Note: `requirements.txt` will be added once the runnable pipeline is implemented.*  
3. Configure `config/email_rules.json` with trusted senders and keywords.  
4. Run initial pipeline (planned placeholder):  
   `python -m pipeline.run`

---

## Configuration


Primary config: `config/email_rules.json`  

```json
{
  "trusted_senders": [],
  "priority_keywords": [
    "internship",
    "hackathon",
    "assignment",
    "deadline"
  ],
  "mode": "balanced"
}
```
- trusted_senders: always treated as important (used in spam recovery).

- priority_keywords: keywords marking emails as important.

- mode: tuning preset (balanced currently).

---

### Outputs & Storage


- reports/: daily reports (e.g., Daily_Productivity_Report.txt)

- logs/: runtime logs

- Documents/AI_Email_Assistant/Important_Mail_Summary.txt: stored summaries for important emails (as described in docs/project_design.md)

--- 

### Usage


- Workflow: update rules → run pipeline → review report → act on flagged emails.
- Outputs: daily markdown reports, cleaned downloads, and logs stored in reports/ and logs/.

--- 

### 🛠 Tech Stack


- Python (core pipeline)
- JSON-based rule engine (config/email_rules.json)
- AI classification & summarization (planned OpenAI integration)
- File system automation (downloads organization)
- Modular pipeline architecture (pipeline/run.py)

---

### Why This Is Different


- Hybrid approach: rule engine handles deterministic decisions; AI handles uncertain cases.
- Config-driven behavior: easily tweak rules via config/email_rules.json.
- Extensible productivity system: can integrate new modules for email, calendar, downloads, or reporting.

---

### Roadmap


- Learning loop for trusted senders
- Calendar integration
- Logging improvements
- Model tuning

---

### Contributing


- Branch naming: feat/<topic> or fix/<issue>
- Open a PR to main with a short summary and testing notes

---

### License


MIT License (placeholder — add LICENSE file when ready)

---

### Demo


Sample daily report snippet:
```
Date: 2026-02-16
Inbox scanned: 42
Spam reviewed: 18 (auto-deleted: 15, kept: 3)
Important flagged: 6
Deadlines found: 2
Downloads organized: 18 files

Highlights
- Internship update: next steps + links
- Hackathon: registration confirmed

Action Items
- Submit Assignment 3 by Feb 20
- RSVP to hackathon kickoff by Feb 18
```

---
