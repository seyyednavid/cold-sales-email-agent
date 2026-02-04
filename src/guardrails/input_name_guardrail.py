from pydantic import BaseModel
from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput

class NameCheckOutput(BaseModel):
    has_personal_name: bool
    detected_name: str | None = None

name_guardrail_agent = Agent(
    name="Personal Name Detector",
    instructions="""
    Decide whether the user's message contains a real person's name (like 'John Smith', 'Sarah Johnson').

    - Job titles like CEO, CTO, Head of Sales are NOT personal names.
    - Company names are NOT personal names.
    Return JSON with:
    - has_personal_name (true/false)
    - detected_name (string or null)
    """,
    output_type=NameCheckOutput,
    model="gpt-4o-mini",
)

@input_guardrail
async def block_personal_names(ctx, agent, message: str):
    result = await Runner.run(name_guardrail_agent, message, context=ctx.context)
    found = result.final_output.has_personal_name

    return GuardrailFunctionOutput(
        output_info={"name_check": result.final_output.model_dump()},
        tripwire_triggered=found
    )
