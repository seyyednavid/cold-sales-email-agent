import os
import requests
from agents import function_tool

@function_tool
def send_email(subject: str, body: str):
    api_key = os.getenv("RESEND_API_KEY")
    to_email = os.getenv("GMAIL_TO")

    if not api_key:
        return {"status": "failure", "message": "RESEND_API_KEY is missing in .env"}
    if not to_email:
        return {"status": "failure", "message": "GMAIL_TO is missing in .env"}

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "from": "ColdReach AI <onboarding@resend.dev>",
        "to": [to_email],
        "subject": subject,
        "html": body,  # body is HTML here
    }

    r = requests.post("https://api.resend.com/emails", json=payload, headers=headers)

    if r.status_code in (200, 202):
        return {"status": "success", "id": r.json().get("id")}
    return {"status": "failure", "status_code": r.status_code, "message": r.text}
