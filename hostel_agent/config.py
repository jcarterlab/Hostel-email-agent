"""Settings for the agent, read from the .env file in the project root."""

import os

from dotenv import load_dotenv

# Reads .env and puts each line into the environment (os.environ).
load_dotenv()


def required(name: str) -> str:
    """Read a setting from .env, and stop with a clear message if it's missing."""
    value = os.getenv(name)
    if not value or value.startswith("paste-your"):
        raise RuntimeError(f"{name} is missing. Paste it into the .env file.")
    return value


# Gemini
GEMINI_API_KEY = required("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")  # optional

# Microsoft (from your app registration in the Entra portal)
MS_CLIENT_ID = required("MS_CLIENT_ID")
