# AI-Productivity-Assistant


**AI-Productivity-Assistant** is a comprehensive productivity automation tool designed to streamline your email workflow, manage your downloads, and create calendar reminders using AI. It integrates Gmail, Google Calendar, and local AI (Ollama) to make your day-to-day tasks seamless and automated.

---

## (IMPORTANT NOTE) :-For detailed Installation Steps and Project Setup refer to "GUIDE.md" file present in this Repository only.

---


## 📝 Quick Guide for Running AI-Productivity-Assistant

### 1️⃣ **Clone Repository**


```bash
git clone https://github.com/<your-username>/AI-Productivity-Assistant.git
cd AI-Productivity-Assistant
```


### 2️⃣ Setup Python Environment


```
python -m venv venv
venv\Scripts\activate.bat   # Windows
pip install -r requirements.txt
```


### 3️⃣ Ollama AI


- Install Ollama CLI / Local Server: http://localhost:11434

- Pull phi3 model:


```
ollama pull phi3
ollama list  # verify model
```


### 4️⃣ Gmail App Password


- Create in Google Account → Security → App Passwords → Mail → Desktop

- Note the 16-digit password for first run authentication.


### 5️⃣ Google Calendar API


- Enable Calendar API in Google Cloud → Desktop OAuth → Add your Gmail under Test Users

- Download JSON → rename to credentials.json → place in config/

- First run → approve consent → token.json auto-generated.

### 6️⃣ Run Project


```
python -m pipeline.run
```


- Enter important keywords and trusted senders when prompted.

- Processes Inbox & Spam, creates calendar events, organizes Downloads, and generates daily report.

### 7️⃣ View Daily Report


```
cat reports/Daily_Productivity_Report.txt
```


### ⚠ Notes


- Run once a day to avoid duplicate calendar events.

- Do not leave empty JSON files in config/.

- Trusted senders are automatically saved for future email recovery.

## 🚀 Features


### 1️⃣ Email Automation


- Scans your **Inbox** and **Spam folder** to detect important emails.
- Flags emails as important based on:
  - **User-defined keywords**.
  - **Trusted senders**.
- **Trusted senders auto-recovery**:  
  Once a sender is added to `trusted_senders` in `email_rules.json`, all future emails from that sender found in the Spam folder are **automatically moved to Inbox** without asking again.
- Rule-based alerts for emails in Spam that match important keywords.
- Generates **daily AI-generated summaries** of important emails using **Ollama AI (phi3 model)**.


### 2️⃣ Calendar Integration


- Detects **dates in important emails**.
- Automatically creates **Google Calendar reminders** one day before the detected date.
- Helps you never miss deadlines or important events.


### 3️⃣ Downloads Folder Cleanup


- Organizes files in your **Downloads** folder into:
  - `Important_College_Docs`
  - `Certificates`
- Uses content analysis (OCR for images, PDF parsing, DOCX, and TXT parsing) to classify files intelligently.
- Renames files based on content for clarity and avoids duplicates.


### 4️⃣ User-Friendly Setup


- GUI-based prompts (fallback to console if GUI is unavailable):
  - Enter **important keywords** one by one.
  - Enter **trusted sender emails**.
- Stores configurations securely in `config/email_rules.json`.
- Gmail credentials stored in `config/email_credentials.json`.
- Google Calendar OAuth token stored in `config/token.json`.

---


## 📂 Project Structure


```
AI-Productivity-Assistant/
├── config/
│   ├── email_credentials.json
│   ├── email_rules.json
│   ├── credentials_google_calendar.json
│   └── token.json
├── docs/
│   └── project_design.md
├── reports/
│   └── Daily_Productivity_Report.txt
├── pipeline/
│   ├── __init__.py
│   ├── spam_processor.py
│   ├── learning_manager.py
│   ├── alert_manager.py
│   ├── email_utils.py
│   ├── calendar_integration.py
│   ├── downloads_cleanup.py
│   ├── ai_summary.py
│   ├── run.py
│   └── user_setup.py
├── skills/
│   └── si-productivity-assistant-dev
│       └── SKILL.md
├── test/
│   ├── conftest.py
│   └── test_run.py
├── README.md
├── GUIDE.md
└── .gitignore
```


## 🧠 Technology Stack


- Python 3.10+

- Libraries: imaplib, email, tkinter, requests, pytesseract, pdfplumber, docx

- Google Calendar API (OAuth 2.0)

- Ollama Local AI (phi3 model)

## 📈 Outputs


- Daily Productivity Report → reports/Daily_Productivity_Report.txt

- Organized Downloads folders: Important_College_Docs, Certificates

- Google Calendar reminders for important email dates

- AI-generated email summary of important emails

- Trusted senders auto-recovery: Emails from trusted senders in Spam are automatically moved to Inbox without alerts.
 

---

