from agents import Agent


def build_subject_writer_agent(model: str = "gpt-4o-mini"):
    subject_instructions = """
You can write a subject for a cold sales email.
You are given a message and you need to write a subject for an email that is likely to get a response.
Return ONLY the subject line.
"""
    return Agent(
        name="Email Subject Writer",
        instructions=subject_instructions,
        model=model
    )


def build_html_converter_agent(model: str = "gpt-4o-mini"):
    html_instructions = """
        Convert the email body into simple HTML for Gmail.

        Rules:
        - Keep everything LEFT aligned (no centered container).
        - Do NOT use buttons.
        - Do NOT add background colors or card layouts.
        - Use only <p>, <br>, <strong> when needed.
        - Return ONLY valid HTML.
        """

    return Agent(
        name="HTML Email Body Converter",
        instructions=html_instructions,
        model=model
    )
