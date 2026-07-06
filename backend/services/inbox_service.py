"""Inbox triage workflow for the FastAPI backend."""
import json
import time
from pathlib import Path

from backend.errors import AppError
from lib import llm

CACHE_JSON = Path("cache/inbox_sample.json")
CATEGORIES = ["Urgent", "Action Needed", "FYI"]

TRIAGE_SYSTEM = """You are an executive assistant triaging an office inbox.
The user pastes raw emails separated by lines containing only ---.
Return a JSON array with exactly one object per email, in the same order:
[{"from": str, "subject": str, "category": "Urgent"|"Action Needed"|"FYI",
  "one_line_summary": str, "suggested_reply": str or null}]
Rules:
- "Urgent" = needs a response today or blocks someone; "Action Needed" = requires
  a decision or task but not immediately; "FYI" = informational only.
- suggested_reply ONLY for Urgent and Action Needed emails; null for FYI.
- Replies must be professional, 3-5 sentences, and ready to send as-is.
- Take "from" and "subject" from the email headers; if missing, infer briefly."""


def clean(items):
    if not isinstance(items, list):
        return []
    cleaned = []
    for item in items:
        if not isinstance(item, dict):
            continue
        category = str(item.get("category", "")).strip()
        if category not in CATEGORIES:
            category = "FYI"
        reply = item.get("suggested_reply")
        cleaned.append({
            "from": str(item.get("from") or "").strip() or "Unknown sender",
            "subject": str(item.get("subject") or "").strip() or "(no subject)",
            "category": category,
            "one_line_summary": str(item.get("one_line_summary", "")).strip(),
            "suggested_reply": str(reply).strip() if reply and category != "FYI" else None,
        })
    return cleaned


def triage(text: str, demo: bool):
    start = time.perf_counter()
    if not text.strip() and not demo:
        raise AppError("Please paste some emails first.")
    provider = "demo"
    if demo:
        try:
            raw = json.loads(CACHE_JSON.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise AppError("Demo cache is missing (cache/inbox_sample.json).") from exc
        except json.JSONDecodeError as exc:
            raise AppError("Demo cache file is corrupted (cache/inbox_sample.json).") from exc
    else:
        n = len([p for p in text.split("---") if p.strip()])
        try:
            raw, provider = llm.ask_claude_json_with_provider(
                TRIAGE_SYSTEM, text, max_tokens=min(500 + 350 * n, 8000)
            )
        except llm.LLMError as exc:
            raise AppError(str(exc), 503) from exc
    emails = clean(raw)
    if not emails:
        raise AppError("Could not extract any emails. Separate emails with --- and try again.")
    return {"emails": emails, "elapsed": time.perf_counter() - start, "provider": provider}
