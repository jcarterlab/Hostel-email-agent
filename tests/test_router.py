"""Tests for the routing logic.

These don't call Gemini. `monkeypatch` temporarily replaces `check_group_booking`
with a fake that returns a fixed answer, so we only test the routing itself.
"""

from hostel_agent import router
from hostel_agent.classifier import GroupBookingCheck
from hostel_agent.router import IGNORE, OWNER_EMAIL, SEND_TO_GROUP, SEND_TO_OWNER, Email, route_email


def pretend_gemini_says(monkeypatch, answer: bool):
    fake_answer = GroupBookingCheck(is_group_booking=answer, reason="fake reason")
    monkeypatch.setattr(router, "check_group_booking", lambda sender, subject, body: fake_answer)


def test_group_asking_for_a_quote_goes_to_owner(monkeypatch):
    pretend_gemini_says(monkeypatch, True)
    email = Email(
        sender="teacher@school.org",
        subject="Group booking enquiry",
        body="Hi, we are a group of 25 students looking to stay 2 nights in March.",
    )
    assert route_email(email).route == SEND_TO_OWNER


def test_owner_replying_with_prices_goes_to_group(monkeypatch):
    pretend_gemini_says(monkeypatch, True)
    email = Email(
        sender=OWNER_EMAIL,
        subject="RE: Group booking enquiry",
        body="£22 per bed per night, breakfast included.",
    )
    assert route_email(email).route == SEND_TO_GROUP


def test_not_a_group_booking_is_ignored(monkeypatch):
    pretend_gemini_says(monkeypatch, False)
    email = Email(
        sender="someone@example.com",
        subject="Lost property",
        body="I think I left my charger in room 4.",
    )
    assert route_email(email).route == IGNORE


def test_decision_includes_geminis_reason(monkeypatch):
    pretend_gemini_says(monkeypatch, True)
    email = Email(sender="teacher@school.org", subject="Trip", body="25 students, 2 nights")
    assert route_email(email).reason == "fake reason"
