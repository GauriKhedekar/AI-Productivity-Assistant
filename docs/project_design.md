# Project Design Document

---

## 1️⃣ System Pipeline

When the system runs:

1. Load configuration file  
2. Scan Spam folder  
3. Apply rule engine (trusted senders + keywords — user-defined only)  
4. AI classification for uncertain emails  
5. Clean Trash  
6. Scan Inbox for important emails  - Scan Inbox for important emails → Generate AI summaries for all important emails
7. Detect deadlines  
8. Organize Downloads folder  
9. Generate daily productivity report  
10. Update trusted senders list if needed  

---

## 2️⃣ Decision Logic (Spam Module)

For each spam email:

- If sender is trusted → Recover  
- Else if keyword matched (user-defined only) → Recover  
- Else AI classify:  
  - High confidence spam → Delete  
  - Medium confidence → Move to Review  
  - Important → Recover  

---

## 3️⃣ Important Mail Intelligence (Hybrid Model + Summary)

Inbox emails are analyzed using a **Hybrid Importance Detection System**:

### Layer 0 — Trusted Senders

For emails from senders listed in `trusted_senders` inside `email_rules.json`:

- Always mark as Important  
- Generate AI summary  
- Save summary in `Important_Mail_Summary.txt`  

This ensures that emails from trusted contacts are **never missed**, even if they contain no keywords.

---

### Layer 1 — User-Defined Keywords

System checks if subject or body contains keywords stored in:

`priority_keywords` inside `email_rules.json`

Examples:
- internship  
- hackathon  
- assignment  
- deadline  

If matched → Mark as Important → Generate AI summary.

---

### Layer 2 — AI-Based Importance Detection

If no keyword matched:

Email is sent to AI with prompt:

"Determine if this email is important for academic, career, or deadline-related activities. Respond with label and confidence score. Summarize the email in 3–4 lines focusing on key action items and dates."

AI returns:
- Important / Not Important  
- Confidence score  
- Summary text  

If confidence ≥ threshold → Mark as Important → Save summary.

---

### Summary Storage

For every important email (trusted-user based or keyword or AI-detected), store summary in:

`Important_Mail_Summary.txt`  

Format:
```
Sender: <email sender>
Subject: <email subject>
Summary: <AI-generated summary>
Detected deadline: <if any>
```
Stored in:

`Documents/AI_Email_Assistant/`

---

## 4️⃣ Deadline Detection

For emails marked Important:

AI extracts:
- Date (if present)
- Event title (from subject)

If valid date detected:
- Create Calendar event
- Add reminder (1 day before)

---

## 5️⃣ Downloads Folder Cleanup

Scan Downloads folder:

- Check filename and optional content preview  
- Move files into folders:  
  - Resume → Resume/  
  - Certificate → Certificates/  
  - Project → Projects/  
  - College / Assignment → College/  
- Optional smart rename if file name messy  

---

## 6️⃣ Learning Loop

If user restores an email from Review:

- Ask user if sender should be trusted  
- If yes → Add to `trusted_senders` in config  
- Save configuration  

This allows adaptive behavior and improves system intelligence over time.

---

## 7️⃣ Report Generation

At the end of execution:

System generates:

`Daily_Productivity_Report.txt`

Containing:

- Spam deleted  
- Spam recovered  
- Important mails detected (trusted-user based + user-defined + AI)  
- Deadlines detected  
- Files organized  
- Trash permanently deleted  

---

## 8️⃣ Key Notes

1. Rule Engine → **trusted senders + user-defined keywords only**  
2. AI → used for **importance detection and summarization**, not for the rule engine  
3. Every important email gets summarized in `Important_Mail_Summary.txt`  
4. Daily report contains **metrics**, summary file contains **actual content**  
5. Emails flagged by AI as Important only if confidence ≥ threshold (configurable)
