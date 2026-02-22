# Project Design - AI-Productivity-Assistant

## Objective
Automate day-to-day productivity tasks:
1. Important email detection and processing
2. Calendar reminder creation
3. Downloads folder organization

---

## System Components

### 1. User Setup
- `pipeline/user_setup.py`:
  - Collects **Gmail credentials**
  - Prompts for **important keywords**
  - Prompts for **trusted sender emails**
  - Stores preferences in `config/email_rules.json`

---

### 2. Email Processing
- `pipeline/spam_processor.py`:
  - Scans **Spam folder** (last 20 emails)
  - Auto-recovers **trusted senders**
  - Alerts user for emails containing priority keywords
  - Updates trusted senders list in `email_rules.json` once that sender is added to the trusted_senders list it will recover all future mails of that trusted_sender    present in spam folder without asking again.
- `pipeline/email_utils.py`:
  - Extracts email body
  - Determines importance by rules or trusted sender

- `pipeline/learning_manager.py`:
  - Manages rules, trusted senders, and ignored keywords

---

### 3. AI Summary
- `pipeline/ai_summary.py`:
  - Uses **Ollama AI phi3** to generate daily email summaries
  - Ensures concise and structured output
  - Summary used in **Daily Productivity Report**

---

### 4. Calendar Integration
- `pipeline/calendar_integration.py`:
  - Scans important emails for dates
  - Creates **Google Calendar events** one day before detected dates
  - Uses Google Calendar API with OAuth 2.0 credentials
  - Token stored as `config/token.json`

---

### 5. Downloads Cleanup
- `pipeline/downloads_cleanup.py`:
  - Creates `Important_College_Docs` and `Certificates` folders
  - Extracts content from files using OCR, PDF, DOCX, and TXT parsers
  - Classifies files based on predefined keywords
  - Renames files based on content
  - Moves files to respective folders

---

### 6. Main Runner
- `pipeline/run.py`:
  - Combines all modules
  - Processes inbox and spam
  - Creates calendar events
  - Organizes downloads
  - Generates **Daily Productivity Report**

---

## Output Files
- `reports/Daily_Productivity_Report.txt` → summary of all processed emails, spam metrics, calendar events, and file organization
- Downloads folders organized:
  - `Important_College_Docs`
  - `Certificates`

---

### Data Flow
1. User inputs → `config/email_rules.json`
2. Emails fetched → Inbox & Spam scanned → Important emails flagged
3. AI generates daily summary → `reports/Daily_Productivity_Report.txt`
4. Important dates → Google Calendar events
5. Downloads folder scanned → Organized & renamed files

---

### Notes
- Modular design for easy extension
- GUI fallback to console ensures usability
- Designed for **solo hackathon**, highly automated and user-friendly
