# Project Design Document

---

## 1️⃣ System Pipeline

When the system runs:

1. Load configuration file  
2. Scan Spam folder  
3. Apply rule engine (trusted senders + user-defined keywords)  
4. AI classification for uncertain emails  
5. Clean Trash  
6. Scan Inbox for important emails  
7. Detect deadlines  
8. Organize Downloads folder  
9. Generate daily productivity report  
10. Update trusted senders list if needed  

---

## 2️⃣ Decision Logic (Spam Module)

For each spam email:

- If sender is trusted → Recover  
- Else if user-defined priority keyword matched → Recover  
- Else AI classify:  
  - High confidence spam → Delete  
  - Medium confidence → Move to Review  
  - Important → Recover  

---

## 3️⃣ Important Mail Intelligence (Hybrid Model)

Inbox emails are analyzed using a **Hybrid Importance Detection System**:

### Layer 1 — User-Defined Keywords

System checks if subject or body contains keywords stored in:

`priority_keywords` inside `email_rules.json`

Examples:
- internship  
- hackathon  
- assignment  
- deadline  

If matched → Mark as Important.

---

### Layer 2 — AI-Based Importance Detection

If no keyword matched:

Email is sent to AI with prompt:

"Determine if this email is important for academic, career, or deadline-related activities. Respond with label and confidence score."

AI returns:
- Important / Not Important
- Confidence score

If confidence ≥ threshold → Mark as Important.

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

## 5️⃣ Learning Loop

If user restores an email from Review:

- Ask user if sender should be trusted  
- If yes → Add to `trusted_senders` in config  
- Save configuration  

This allows adaptive behavior and improves system intelligence over time.

---

## 6️⃣ Report Generation

At the end of execution:

System generates:

`Daily_Productivity_Report.txt`

Containing:

- Spam deleted  
- Spam recovered  
- Important mails detected (keyword + AI)  
- Deadlines detected  
- Files organized  
- Trash permanently deleted  
