"""Single shared LLM wrapper. Every API call in OfficeFlow goes through here."""
import json
import os
import urllib.error
import urllib.request

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash"
GROQ_MODEL = "llama-3.3-70b-versatile"
OPENROUTER_MODEL = "openrouter/auto"
PROVIDER_ORDER = ("gemini", "groq", "openrouter")
DEMO_HINT = "For the live demo, you can turn on Demo Mode in the sidebar."


class LLMError(Exception):
    """Raised when all configured providers fail. The message is safe to show."""


_client = None


def _load_api_key() -> str | None:
    return _load_key("GEMINI_API_KEY")


def _load_key(name: str) -> str | None:
    try:
        key = st.secrets[name]
        if key:
            return str(key)
    except Exception:
        pass
    load_dotenv()
    return os.getenv(name)


def _get_client():
    global _client
    if _client is None:
        key = _load_api_key()
        if not key or key == "your_key_here":
            raise LLMError(
                "Gemini API key is missing. Add GEMINI_API_KEY in "
                f"Streamlit secrets or your local .env file. {DEMO_HINT}"
            )
        _client = genai.Client(api_key=key)
    return _client


def _gemini(system: str, user: str, max_tokens: int, response_mime_type=None) -> str:
    config_args = {"system_instruction": system, "max_output_tokens": max_tokens}
    if response_mime_type:
        config_args["response_mime_type"] = response_mime_type
    response = _get_client().models.generate_content(
        model=MODEL,
        contents=user,
        config=types.GenerateContentConfig(**config_args),
    )
    return getattr(response, "text", "")


def _chat_payload(model: str, system: str, user: str, max_tokens: int) -> bytes:
    return json.dumps(
        {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "max_tokens": max_tokens,
        }
    ).encode("utf-8")


def _openai_compatible(provider: str, system: str, user: str, max_tokens: int) -> str:
    if provider == "groq":
        key = _load_key("GROQ_API_KEY")
        url = "https://api.groq.com/openai/v1/chat/completions"
        model = GROQ_MODEL
    else:
        key = _load_key("OPENROUTER_API_KEY")
        url = "https://openrouter.ai/api/v1/chat/completions"
        model = OPENROUTER_MODEL
    if not key:
        raise LLMError(f"{provider} API key is missing.")
    request = urllib.request.Request(
        url,
        data=_chat_payload(model, system, user, max_tokens),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5173",
            "X-Title": "OfficeFlow",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return str(payload["choices"][0]["message"]["content"])


def _call_provider(provider: str, system: str, user: str, max_tokens: int,
                   response_mime_type=None) -> str:
    if provider == "gemini":
        return _gemini(system, user, max_tokens, response_mime_type)
    return _openai_compatible(provider, system, user, max_tokens)


def _provider_enabled(provider: str) -> bool:
    if provider == "gemini":
        return True
    key_name = {
        "groq": "GROQ_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
    }[provider]
    return bool(_load_key(key_name))


def _friendly_failure(provider: str, exc: Exception) -> str:
    if isinstance(exc, LLMError):
        return str(exc)
    if isinstance(exc, (urllib.error.URLError, TimeoutError)):
        return f"{provider} request failed. Check your internet connection."
    return f"{provider} request failed ({type(exc).__name__})."


def _generate(system: str, user: str, max_tokens: int,
              response_mime_type=None) -> tuple[str, str]:
    failures = []
    for provider in PROVIDER_ORDER:
        if not _provider_enabled(provider):
            failures.append(f"{provider}: API key missing")
            continue
        try:
            text = _call_provider(provider, system, user, max_tokens, response_mime_type)
            if text and text.strip():
                return text, provider
            failures.append(f"{provider}: empty response")
        except Exception as exc:
            failures.append(f"{provider}: {_friendly_failure(provider, exc)}")
    detail = "; ".join(failures) or "no providers configured"
    raise LLMError(f"All AI providers failed ({detail}). {DEMO_HINT}")


def ask_claude(
    system: str,
    user: str,
    max_tokens: int = 2000,
    response_mime_type: str | None = None,
) -> str:
    """Send one prompt to the configured provider cascade."""
    return _generate(system, user, max_tokens, response_mime_type)[0]


def ask_claude_with_provider(
    system: str,
    user: str,
    max_tokens: int = 2000,
    response_mime_type: str | None = None,
) -> tuple[str, str]:
    """Send one prompt and return (text, provider_name)."""
    return _generate(system, user, max_tokens, response_mime_type)


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
    return ask_claude_json_with_provider(system, user, max_tokens)[0]


def ask_claude_json_with_provider(system: str, user: str, max_tokens: int = 2000):
    """Return (parsed_json, provider_name), falling back on invalid JSON."""
    json_system = (
        system
        + "\n\nRespond with valid JSON only. No explanations, no markdown fences."
    )
    failures = []
    for provider in PROVIDER_ORDER:
        if not _provider_enabled(provider):
            failures.append(f"{provider}: API key missing")
            continue
        try:
            raw = _call_provider(provider, json_system, user, max_tokens,
                                 response_mime_type="application/json")
            return json.loads(_strip_fences(raw)), provider
        except json.JSONDecodeError:
            failures.append(f"{provider}: invalid JSON")
        except Exception as exc:
            failures.append(f"{provider}: {_friendly_failure(provider, exc)}")
    detail = "; ".join(failures) or "no providers configured"
    raise LLMError(f"All AI providers failed ({detail}). {DEMO_HINT}")
