# 🚀 AI Productivity Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue?logo=python">
  <img src="https://img.shields.io/badge/Automation-AI%20Powered-success">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen">
</p>

---

## 📌 Overview

**AI Productivity Assistant** is an intelligent automation system designed to streamline your daily workflow by integrating:

* 📧 Email Management (Gmail)
* 📅 Smart Calendar Scheduling (Google Calendar)
* 🧠 AI-powered summarization (Ollama - phi3)
* 📂 Automatic Downloads Organization

This system reduces manual effort by automating repetitive tasks and intelligently organizing your digital workspace.

---

## 🎯 Problem Statement

Managing emails, tracking important dates, and organizing downloads manually is time-consuming and inefficient.

👉 This project solves that by:

* Automatically detecting important emails
* Creating calendar reminders
* Organizing files intelligently
* Generating AI-based summaries

---

## 🚀 Features

### 📧 Email Automation

* Scans **Inbox & Spam folders**
* Detects important emails using:

  * Keywords
  * Trusted senders
* Auto-recovers emails from Spam
* Generates **AI-based email summaries**

---

### 📅 Smart Calendar Integration

* Detects dates from emails
* Automatically schedules reminders
* Prevents missed deadlines

---

### 📂 Intelligent File Management

* Organizes Downloads into:

  * `Important_College_Docs`
  * `Certificates`
* Uses OCR + file parsing (PDF, DOCX, TXT)
* Avoids duplicate files

---

### 🧠 AI Integration

* Uses **Ollama (phi3 model)**
* Generates summaries of important emails
* Enhances productivity with local AI

---

## 🏗 System Architecture

```
User Input
   │
   ▼
Email Processing (IMAP)
   │
   ▼
AI Analysis (Ollama)
   │
   ├── Email Summary
   ├── Important Detection
   ▼
Calendar Integration (Google API)
   │
   ▼
File Management (Downloads Cleanup)
   │
   ▼
Daily Productivity Report
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/<your-username>/AI-Productivity-Assistant.git
cd AI-Productivity-Assistant
```

---

### 2️⃣ Setup Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

### 3️⃣ Setup Ollama AI

* Install Ollama: http://localhost:11434

```bash
ollama pull phi3
ollama list
```

---

### 4️⃣ Gmail Configuration

* Enable **App Passwords**
* Generate 16-digit password
* Use it for authentication

---

### 5️⃣ Google Calendar Setup

* Enable Calendar API
* Download credentials JSON
* Place inside `config/`
* First run will generate `token.json`

---

### 6️⃣ Run Application

```bash
python -m pipeline.run
```

---

## 📊 Outputs

* 📄 Daily Productivity Report
* 📅 Calendar Reminders
* 📂 Organized Downloads
* 🧠 AI Email Summary

---

## 📂 Project Structure

```
AI-Productivity-Assistant/
├── config/
├── docs/
├── reports/
├── pipeline/
├── skills/
├── test/
├── README.md
├── GUIDE.md
└── .gitignore
```

---

## 🛠 Tech Stack

* **Python 3.10+**
* Google Calendar API
* Ollama (Local AI)
* OCR (pytesseract)
* PDF & Document Processing

---

## 🔮 Future Improvements

* Web Dashboard (Streamlit / React)
* Email classification using Deep Learning
* Notification system (SMS / WhatsApp)
* Cloud deployment support

---

## 👨‍💻 Author

**Gauri Khedekar**

---

## ⭐ Contribution

Contributions are welcome!
Feel free to fork this repo and submit a pull request.

---
