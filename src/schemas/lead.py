from pydantic import BaseModel, EmailStr
from typing import Optional


class Lead(BaseModel):
    """
    Structured input for a cold email lead.
    This helps your agents write more accurate emails
    without placeholders.
    """

    # Who are we emailing?
    company: str
    role: str = "CEO"
    first_name: Optional[str] = None

    # Context about the lead / company
    industry: Optional[str] = None
    pain_point: Optional[str] = None
    website: Optional[str] = None

    # Optional contact email (if you want to send directly later)
    email: Optional[EmailStr] = None

    def to_prompt(self) -> str:
        """
        Convert structured lead info into a clean prompt
        for your agents.
        """
        parts = [
            f"Company: {self.company}",
            f"Role: {self.role}",
        ]

        if self.first_name:
            parts.append(f"First name: {self.first_name}")

        if self.industry:
            parts.append(f"Industry: {self.industry}")

        if self.pain_point:
            parts.append(f"Pain point: {self.pain_point}")

        if self.website:
            parts.append(f"Website: {self.website}")

        return "\n".join(parts)
