"""Single shared Claude client. Every API call in OfficeFlow goes through here."""
import json
import os

import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv

MODEL = "claude-sonnet-4-6"
DEMO_HINT = "For the live demo, you can turn on Demo Mode in the sidebar."


class LLMError(Exception):
    """Raised when a Claude call fails. The message is safe to show in the UI."""


_client = None


def _load_api_key() -> str | None:
    try:
        key = st.secrets["ANTHROPIC_API_KEY"]
        if key:
            return str(key)
    except Exception:
        pass
    load_dotenv()
    return os.getenv("ANTHROPIC_API_KEY")


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        key = _load_api_key()
        if not key or key == "your_key_here":
            raise LLMError(
                "Anthropic API key is missing. Add ANTHROPIC_API_KEY in "
                f"Streamlit secrets or your local .env file. {DEMO_HINT}"
            )
        _client = Anthropic(api_key=key)
    return _client


def ask_claude(system: str, user: str, max_tokens: int = 2000) -> str:
    """Send one prompt to Claude and return the text of the reply."""
    try:
        response = _get_client().messages.create(
            model=MODEL,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
    except LLMError:
        raise
    except Exception as exc:
        raise LLMError(
            f"Claude request failed ({type(exc).__name__}). "
            f"Check your internet connection and API key, then try again. {DEMO_HINT}"
        ) from exc
    text = "".join(block.text for block in response.content if block.type == "text")
    if not text.strip():
        raise LLMError(f"Claude returned an empty response. Please try again. {DEMO_HINT}")
    return text


def _strip_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        newline = text.find("\n")
        text = text[newline + 1:] if newline != -1 else ""
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]
    return text.strip()


def ask_claude_json(system: str, user: str, max_tokens: int = 2000):
    """Like ask_claude, but demands JSON-only output and returns the parsed value."""
    json_system = (
        system
        + "\n\nRespond with valid JSON only. No explanations, no markdown fences."
    )
    raw = ask_claude(json_system, user, max_tokens)
    try:
        return json.loads(_strip_fences(raw))
    except json.JSONDecodeError as exc:
        raise LLMError(
            "Claude returned data that could not be parsed as JSON. "
            f"Please try again. {DEMO_HINT}"
        ) from exc
