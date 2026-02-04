from agents import Agent
from tools.resend_tool import send_email


def build_email_manager_send(model: str = "gpt-4o-mini"):
    return Agent(
        name="Email Sender",
        instructions="""
You receive:

SUBJECT:
...

HTML:
...

Call send_email exactly ONCE using subject + html.
Return only: SENT or FAILED.
""",
        tools=[send_email],
        model=model,
    )
