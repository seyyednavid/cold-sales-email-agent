import streamlit as st
import asyncio
from dotenv import load_dotenv
from agents import Runner, trace

from my_agents.sales_agents import build_sales_agents
from my_agents.sales_manager_agent import build_sales_manager
from my_agents.email_manager_agent import build_email_manager


# -------------------------
# Helper to run async in Streamlit
# -------------------------
def run_async(coro):
    return asyncio.run(coro)


# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Cold Sales Email Agent", layout="wide")
st.title("📩 Cold Sales Email Agent (TaskFlow AI)")

load_dotenv(override=True)

# -------------------------
# Inputs
# -------------------------
company = st.text_input("Lead Company", value="FinTrust")
role = st.text_input("Lead Role", value="CEO")
industry = st.text_input("Industry", value="FinTech")
pain_point = st.text_area(
    "Pain Point",
    value="Teams waste time in status meetings because updates and progress tracking are not automated"
)

to_email = st.text_input("Send To (GMAIL_TO in .env will be used by Resend)", value="")

# -------------------------
# Session storage
# -------------------------
if "preview_body" not in st.session_state:
    st.session_state.preview_body = ""

if "preview_ready" not in st.session_state:
    st.session_state.preview_ready = False


# -------------------------
# Build Agents (only once)
# -------------------------
sales_agent1, sales_agent2, sales_agent3 = build_sales_agents()

tools = [
    sales_agent1.as_tool("sales_agent1", "Write a cold sales email"),
    sales_agent2.as_tool("sales_agent2", "Write a cold sales email"),
    sales_agent3.as_tool("sales_agent3", "Write a cold sales email"),
]

email_manager = build_email_manager()

sales_manager = build_sales_manager(
    tools=tools,
    handoffs=[]  # IMPORTANT: we do NOT handoff automatically in preview mode
)


# -------------------------
# Preview Button
# -------------------------
if st.button("👀 Generate Preview Email"):
    message = f"""
Write a cold sales email.

Lead company: {company}
Lead role: {role}
Industry: {industry}
Pain point: {pain_point}

Rules:
- Return ONLY the plain email BODY.
- Do NOT include Subject.
- Do NOT include HTML.
- Do NOT include placeholders like [Your Name].
"""

    with st.spinner("Generating best email draft..."):
        with trace("ColdReach - UI Preview"):
            result = run_async(Runner.run(sales_manager, message, max_turns=20))

    st.session_state.preview_body = result.final_output.strip()
    st.session_state.preview_ready = True

    st.success("✅ Preview generated!")


# -------------------------
# Show Preview Output
# -------------------------
st.subheader("📌 Preview Result (Plain Body Only)")
preview_text = st.text_area(
    "Final Output",
    value=st.session_state.preview_body,
    height=300
)


# -------------------------
# Send Button
# -------------------------
if st.session_state.preview_ready:
    if st.button("📨 Send Email"):
        if not preview_text.strip():
            st.error("❌ Preview email body is empty.")
        else:
            with st.spinner("Sending email..."):
                with trace("ColdReach - UI Send"):
                    send_result = run_async(Runner.run(email_manager, preview_text.strip(), max_turns=20))

            st.success("✅ Email sent successfully!")
            st.write(send_result.final_output)
