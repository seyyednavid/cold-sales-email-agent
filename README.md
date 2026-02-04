# 📩 Cold Sales Email Agent (TaskFlow AI)

A multi-agent cold email generator built with **OpenAI Agents SDK + Streamlit + Resend API**.

This project generates 3 cold email drafts using different writing styles, selects the best one, validates/fixes it automatically, shows a preview in the UI, and only sends the email when the user clicks **Send Email**.

---

## 🚀 Features

✅ 3 Sales Agents generate different cold email drafts  
✅ Sales Manager picks the best draft automatically  
✅ Email Manager Preview validates + fixes + formats (subject + HTML)  
✅ Streamlit UI for entering lead details  
✅ Email is only sent when user clicks **Send Email**  
✅ Resend API integration for delivery  

---

## 🧠 Agent Workflow (Architecture)

### 1) Input Guardrail
Blocks personal names in the user prompt to prevent privacy issues.

Blocked input example:
- Send email to John Smith ❌

Allowed input example:
- Send email to Dear CEO ✅

### 2) Sales Manager Agent
The Sales Manager controls the writing process:
1. Calls `sales_agent1` → Draft 1  
2. Calls `sales_agent2` → Draft 2  
3. Calls `sales_agent3` → Draft 3  
4. Chooses the best draft  
5. Hands off the final draft to **Email Manager Preview**

### 3) Email Manager Preview Agent
The Preview agent ensures the email is safe and sendable before sending:

1. `validate_email(body=...)`
2. If validation fails:
   - `fix_email(body=...)`
   - validate again
   - if still failing → **STOP** (do not send)
3. Generate subject line → `subject_tool`
4. Convert email body to HTML → `html_tool`
5. Return the final preview result to the UI (Subject + Body + HTML)

### 4) Email Manager Send Agent
This agent only runs when the user clicks **Send Email** in the UI:

1. Receives the final subject + HTML
2. Sends email using Resend → `send_email`

---

## 🧪 Validation Rules

Before sending, the email must:

✅ be under **200 words**  
✅ include a CTA (Call To Action) such as **10–15 minute call**  
✅ contain **no placeholders**, such as:

- `[Your Name]`
- `(Your Phone Number)`
- `{{company}}`

If validation fails, the system tries to fix it automatically.  
If it still fails after fixing, the email will **NOT** be sent.

---

## 🖥️ Streamlit UI

The UI allows you to enter:

- Lead Company
- Lead Role
- Industry
- Pain Point
- (Optional) Send-to email

Then you click:

✅ **Generate Preview** → see the final output (subject + body + html)  
✅ **Send Email** → sends the email using Resend API  

---

## ⚙️ Setup Instructions

### 1) Clone the project
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2) Create and activate a virtual environment

Windows (PowerShell)

python -m venv .venv
.venv\Scripts\Activate


macOS / Linux

python3 -m venv .venv
source .venv/bin/activate

### 3) Install dependencies
pip install -r requirements.txt


### 🔑 Environment Variables

Create a .env file in the project root.

.env.example
OPENAI_API_KEY=
RESEND_API_KEY=
GMAIL_TO=


Then create your local .env (do not commit it):

OPENAI_API_KEY=your_openai_key_here
RESEND_API_KEY=your_resend_key_here
GMAIL_TO=your_email_here

### ▶️ Run the Project (Streamlit UI)
streamlit run src/app.py

### 📨 Email Sending (Resend)

Emails are sent using the Resend API.

⚠️ In production, you should verify your domain and use a verified sender email.

### 📌 Notes

- Sales agents are converted into tools so the Sales Manager can call them reliably.
- Validation is performed before sending to avoid sending emails with placeholders.
- The Email Manager Preview is responsible for validation + formatting.
- The Email Manager Send agent is responsible for delivery only.

🚀 Future Improvements (Planned)

- Store email history (SQLite / Postgres)
- Lead schema support (structured input)
- A/B testing analytics (open rate, reply rate)



### ⚠️ Disclaimer

This project is for educational/demo purposes.
Do not use it to spam users or violate email marketing laws (GDPR, CAN-SPAM).


