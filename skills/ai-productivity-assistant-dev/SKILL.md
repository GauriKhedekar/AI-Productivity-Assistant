
---

## **SKILL.md**

```markdown
# Skill - AI-Productivity-Assistant

## Overview
AI-Productivity-Assistant is a **productivity automation skill** designed to automate your daily email workflow, manage downloads, and create reminders using AI.

### Key Capabilities
1. **Email Automation**
   - Flags important emails based on **keywords** and **trusted senders**.
   - Processes **Spam folder**:
     - Prompts user for important emails
     - Auto-recovers trusted emails
     - Deletes irrelevant spam
   - Generates **daily AI summary** of important emails using **Ollama AI**.

2. **Calendar Integration**
   - Detects **dates in emails** flagged as important.
   - Creates **Google Calendar reminders** one day before the event.

3. **Downloads Cleanup**
   - Organizes files in `Downloads` folder into:
     - `Important_College_Docs`
     - `Certificates`
   - Uses content analysis (OCR + PDF/DOCX/Text parsing) to classify files.
   - Renames files based on content for clarity.

4. **User-Friendly Setup**
   - GUI-based prompts for entering important keywords and trusted senders.
   - Stores configurations securely in `config/email_rules.json` and credentials in `config/email_credentials.json`.

### Technology Stack
- Python 3.10+
- Libraries: `imaplib`, `email`, `tkinter`, `requests`, `pytesseract`, `pdfplumber`, `docx`
- Google Calendar API
- Ollama local AI server (`phi3` model)

### Inputs
- Gmail account + App Password
- Google Calendar credentials
- Important keywords (emails)
- Trusted sender emails

### Outputs
- Daily report: `reports/Daily_Productivity_Report.txt`
- Organized Downloads folders
- Google Calendar reminders
- AI-generated summary of important emails
