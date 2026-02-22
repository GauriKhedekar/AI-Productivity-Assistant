GUIDE.md
# AI-Productivity-Assistant - GUIDE


This guide explains step-by-step how to set up and run **AI-Productivity-Assistant** locally. It is intended for both users and hackathon judges testing the project.


---


## 1️⃣ Fork & Clone Repository


1. Fork the repository on GitHub.
2. Clone it to your local machine:
```bash
git clone https://github.com/<your-username>/AI-Productivity-Assistant.git
cd AI-Productivity-Assistant
```


## 2️⃣ Setup Python Environment


1. Run the following commands in Command Prompt (not PowerShell)

```
python -m venv venv
Venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

This will create a virtual environment and install all dependencies.


## 3️⃣ Ollama AI Setup


1. Install Ollama CLI / Local Server

2. Visit Ollama website and follow installation instructions for your OS.

3. Make sure the server is running at: http://localhost:11434.

4. Pull the phi3 model

```
ollama pull phi3
```

5.Verify Installation

```
ollama list
```

You should see the phi3 model listed.


## 4️⃣ Gmail App Password Setup


1. Go to Google Account Security

```
 → App Passwords -> Select Mail → Windows Computer (or your platform) → Generate.
```

2. Copy the 16-digit password and store it securely as you will be asked for this password during project initialization.

- ⚠ Note: Use Gmail address + App Password in the first run for authentication.


## 5️⃣ Google Calendar API Setup


1. Go to Google Cloud Console
   
```
Create a new project. -> Enable Google Calendar API. -> Create OAuth 2.0 Client ID credentials → Application Type: Desktop app. -> Add your Gmail account under Test Users in OAuth consent screen.
```

2. Download the JSON credentials → rename to credentials_google_calendar.json.

3. Place it in config/ folder of the project.

4. On first run, approve consent when prompted → token.json will be auto-generated.


## 6️⃣ Run the Project


```
python -m pipeline.run
``` 

1. You will be prompted to enter:

- Important keywords (one by one)

- Trusted senders (emails one by one)

2. The script will process:

- Inbox and Spam emails

- Generate daily email summary and store it in Daily_Productivity_Report.txt

- Create Google Calendar events for important emails

- Organize Downloads folder


## 7️⃣ View Daily Report


```
cat reports/Daily_Productivity_Report.txt
```

The report contains:

- Inbox scanned

- Spam reviewed, recovered, deleted

- Calendar events created

- Files organized

- AI-generated email summary


### ⚠ Things to Remember


- Do not keep empty JSON files in the config/ folder.

- Run the project once a day to avoid duplicate calendar events.

- To avoid duplicates, you may enhance code to check if a calendar event already exists for an email.


---

