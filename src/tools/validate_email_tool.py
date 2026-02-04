import re
from agents import function_tool

MAX_WORDS = 200

PLACEHOLDER_REGEX = re.compile(
    r"\[[^\]]+\]|\([^)]+\)|\{\{.*?\}\}",
    re.IGNORECASE
)


CTA_REGEX = re.compile(
    r"\b(10|15)\s*(min|minutes)\b|\bquick call\b|\bshort call\b|\bbrief call\b|\bchat\b|\bcall\b",
    re.IGNORECASE
)

def validate_email_text(body: str) -> dict:
    word_count = len(re.findall(r"\b\w+\b", body))
    too_long = word_count > MAX_WORDS
    has_placeholders = PLACEHOLDER_REGEX.search(body) is not None
    has_cta = CTA_REGEX.search(body) is not None

    reasons = []
    if too_long:
        reasons.append("too_long")
    if has_placeholders:
        reasons.append("placeholders")
    if not has_cta:
        reasons.append("missing_cta")

    return {"ok": len(reasons) == 0, "reasons": reasons, "word_count": word_count}

@function_tool
def validate_email(body: str) -> dict:
    return validate_email_text(body)
