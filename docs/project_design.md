# Project Design Document

---

## 1️⃣ System Pipeline

When the system runs:

1. Load configuration file  
2. Scan Spam folder  
3. Apply rule engine (trusted senders + keywords)  
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
- Else if keyword matched → Recover  
- Else AI classify:  
  - High confidence spam → Delete  
  - Medium confidence → Move to Review  
  - Important → Recover  

---

## 3️⃣ Learning Loop

If user restores an email from Review:

- Ask user if sender should be trusted  
- If yes → Add to `trusted_senders` in config  
- Save configuration  

This allows adaptive behavior and improves system intelligence over time.

---

## 4️⃣ Report Generation

At the end of execution:

System generates:

`Daily_Productivity_Report.txt`

Containing:

- Spam deleted  
- Spam recovered  
- Important mails found  
- Deadlines detected  
- Files organized  

