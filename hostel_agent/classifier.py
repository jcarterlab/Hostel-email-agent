"""Ask Gemini whether an email is about a group booking."""

from google import genai
from pydantic import BaseModel, Field

from hostel_agent.config import GEMINI_API_KEY, GEMINI_MODEL

PROMPT = """You work at a hostel and sort incoming emails.

Decide if this email is about a GROUP BOOKING. That includes:
- a group (school, team, tour, club, family gathering, etc.) asking for a quote or availability
- a reply from the hostel owner giving prices for a group

It does NOT include single or small private bookings, lost property,
newsletters, invoices, or anything else.

From: {sender}
Subject: {subject}

{body}
"""


# The shape of the answer we want back. Gemini is told to reply with JSON
# that matches this, and Pydantic checks it and turns it into a Python object.
class GroupBookingCheck(BaseModel):
    is_group_booking: bool
    reason: str = Field(description="One short sentence explaining the decision.")


def check_group_booking(sender: str, subject: str, body: str) -> GroupBookingCheck:
    client = genai.Client(api_key=GEMINI_API_KEY)

    interaction = client.interactions.create(
        model=GEMINI_MODEL,
        input=PROMPT.format(sender=sender, subject=subject, body=body),
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": GroupBookingCheck.model_json_schema(),
        },
    )

    return GroupBookingCheck.model_validate_json(interaction.output_text)
