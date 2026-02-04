from agents import Agent

def build_fix_email_agent(model: str = "gpt-4o-mini"):
    return Agent(
        name="Email Fixer",
        instructions="""
            You rewrite a cold email body to pass validation.

            Fix these issues if present:
            - Remove ANY placeholders, including:
            [Your Name], (Your Title), (Your Email Address), (Your Phone Number), {{company}}, etc.
            - Remove any signature fields like title/email/phone.
            - Keep <= 200 words.
            - Must end with a simple CTA asking for a 10–15 minute call.

            Signature rule:
            - End ONLY with: "Best regards,\nTaskFlow AI"

            Return ONLY the fixed plain-text email body.
            """,
        model=model
    )
