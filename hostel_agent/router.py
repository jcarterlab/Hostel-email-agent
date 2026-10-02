"""Decide what to do with an incoming email.

Two questions, in order:
  1. Is this email about a group booking?  (Gemini decides)
  2. If so, who is the next email for: the owner, or the group?
"""

from dataclasses import dataclass

from hostel_agent.classifier import check_group_booking

OWNER_EMAIL = "jack@mosaique.co.uk"

# The three possible outcomes.
IGNORE = "ignore"                      # not a group booking - leave it alone
SEND_TO_OWNER = "send_to_owner"        # a group wants a quote - ask the owner for prices
SEND_TO_GROUP = "send_to_group"        # the owner sent prices - make a quote for the group


@dataclass
class Email:
    sender: str
    subject: str
    body: str


@dataclass
class RoutingDecision:
    route: str   # one of the three outcomes above
    reason: str  # Gemini's explanation, so we can see why


def route_email(email: Email) -> RoutingDecision:
    # Question 1: is it about a group booking? Gemini is asked exactly once.
    check = check_group_booking(email.sender, email.subject, email.body)
    if not check.is_group_booking:
        return RoutingDecision(IGNORE, check.reason)

    # Question 2: who is it from?
    if email.sender.lower() == OWNER_EMAIL:
        return RoutingDecision(SEND_TO_GROUP, check.reason)

    return RoutingDecision(SEND_TO_OWNER, check.reason)
