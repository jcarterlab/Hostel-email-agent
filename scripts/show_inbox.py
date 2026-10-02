"""Print the 10 newest emails in your Outlook inbox. Doesn't change anything.

Run it from the project root:
    .venv/Scripts/python scripts/show_inbox.py
"""

from hostel_agent.mailbox import fetch_recent_emails

for email in fetch_recent_emails(10):
    print(f"From:    {email.sender}")
    print(f"Subject: {email.subject}")
    print(f"Body:    {email.body[:150].strip()}...")  # just the first 150 characters
    print()
