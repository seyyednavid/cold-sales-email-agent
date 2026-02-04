from agents import Agent
from guardrails.input_name_guardrail import block_personal_names


instructions = """
You are a Sales Manager at TaskFlow AI.

Steps (do exactly once):
1) Call sales_agent1 tool ONCE.
2) Call sales_agent2 tool ONCE.
3) Call sales_agent3 tool ONCE.
4) Pick the best ONE email.
5) Handoff the winning email to Email Manager ONCE.

Rules:
- Never call any sales tool more than once.
- Do not retry or regenerate.
- Do not fix the email.
- Do not validate.
- Output only the winning draft in the handoff.
- Stop immediately after handoff.
"""



def build_sales_manager(tools, handoffs, model: str = "gpt-4o-mini"):
    return Agent(
        name="Sales Manager",
        instructions=instructions,
        tools=tools,
        handoffs=handoffs,
        input_guardrails=[block_personal_names],
        model=model,
    )
