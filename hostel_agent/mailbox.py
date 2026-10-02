"""Read emails from Outlook using the Microsoft Graph API.

The reception mailbox is a personal Outlook.com account, so someone has to sign
in to it once (the "device code" flow). The sign-in is then saved and reused.

Two steps:
  1. get_access_token()     - sign in to Microsoft and get a "pass" for the API
  2. fetch_recent_emails()  - use that pass to read the inbox
"""

import os

import msal
import requests

from hostel_agent.config import MS_CLIENT_ID
from hostel_agent.router import Email

GRAPH_URL = "https://graph.microsoft.com/v1.0"

# "consumers" = Microsoft's sign-in for personal accounts (outlook.com, hotmail.com).
AUTHORITY = "https://login.microsoftonline.com/consumers"

# What we're asking permission to do. Mail.ReadWrite = read emails and create drafts.
SCOPES = ["Mail.ReadWrite"]

# Your sign-in is saved here so you only need to log in once. Keep it secret.
TOKEN_CACHE_FILE = "token_cache.json"


def get_access_token() -> str:
    # Load the saved sign-in, if there is one.
    cache = msal.SerializableTokenCache()
    if os.path.exists(TOKEN_CACHE_FILE):
        with open(TOKEN_CACHE_FILE) as f:
            cache.deserialize(f.read())

    app = msal.PublicClientApplication(MS_CLIENT_ID, authority=AUTHORITY, token_cache=cache)

    # Try the saved sign-in first. This needs no input from you.
    result = None
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])

    # Nothing saved (or it expired): sign in by typing a code into your browser.
    if not result:
        flow = app.initiate_device_flow(scopes=SCOPES)
        if "user_code" not in flow:
            raise RuntimeError(f"Could not start sign-in: {flow.get('error_description')}")
        print(flow["message"])  # tells you which website to open and which code to type
        result = app.acquire_token_by_device_flow(flow)  # waits until you've signed in

    if "access_token" not in result:
        raise RuntimeError(f"Sign-in failed: {result.get('error_description')}")

    # Save the sign-in for next time.
    if cache.has_state_changed:
        with open(TOKEN_CACHE_FILE, "w") as f:
            f.write(cache.serialize())

    return result["access_token"]


def fetch_recent_emails(count: int = 10) -> list[Email]:
    response = requests.get(
        f"{GRAPH_URL}/me/mailFolders/inbox/messages",  # "me" = whoever signed in
        headers={
            "Authorization": f"Bearer {get_access_token()}",
            "Prefer": 'outlook.body-content-type="text"',  # plain text, not HTML
        },
        params={
            "$top": count,                          # how many emails
            "$select": "from,subject,body",         # only the fields we need
            "$orderby": "receivedDateTime desc",    # newest first
        },
    )
    response.raise_for_status()  # stop with an error if Microsoft said no

    # Turn each Outlook message into our own simple Email object.
    emails = []
    for message in response.json()["value"]:
        emails.append(
            Email(
                sender=message["from"]["emailAddress"]["address"],
                subject=message["subject"],
                body=message["body"]["content"],
            )
        )
    return emails
