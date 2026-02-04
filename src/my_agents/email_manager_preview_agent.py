from agents import Agent
from tools.validate_email_tool import validate_email
from my_agents.fix_email_agent import build_fix_email_agent
from my_agents.formatting_agents import build_subject_writer_agent, build_html_converter_agent


def build_email_manager_preview(model: str = "gpt-4o-mini"):
    fix_agent = build_fix_email_agent(model=model)

    subject_writer = build_subject_writer_agent(model=model)
    html_converter = build_html_converter_agent(model=model)

    fix_tool = fix_agent.as_tool("fix_email", "Fix the email body to pass validation")
    subject_tool = subject_writer.as_tool("subject_writer", "Write a subject line")
    html_tool = html_converter.as_tool("html_converter", "Convert plain text to HTML")

    return Agent(
        name="Email Manager Preview",
        handoff_description="Validates and formats email for preview (no sending).",
        instructions="""
You receive ONE cold email body (plain text).

Flow:
1) Call validate_email(body=...)
2) If ok=false:
   - call fix_email(body=...)
   - validate again
   - if still ok=false: STOP and output "VALIDATION_FAILED: <reasons>"
3) Generate subject with subject_writer
4) Convert body to HTML with html_converter
5) Output this exact format:

SUBJECT:
<subject>

BODY:
<plain text body>

HTML:
<html body>
""",
        tools=[validate_email, fix_tool, subject_tool, html_tool],
        model=model,
    )
