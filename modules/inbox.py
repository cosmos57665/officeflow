"""Module 2: Inbox — paste raw emails, one Gemini call triages them into three columns."""
import json
import time
from pathlib import Path

import streamlit as st

from lib import llm

SAMPLE_TXT = Path("samples/emails.txt")
CACHE_JSON = Path("cache/inbox_sample.json")

CATEGORIES = ["Urgent", "Action Needed", "FYI"]
STYLES = {
    "Urgent": "Urgent",
    "Action Needed": "Action Needed",
    "FYI": "FYI",
}

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


def _load_sample():
    try:
        st.session_state["inbox_text"] = SAMPLE_TXT.read_text(encoding="utf-8")
    except FileNotFoundError:
        st.session_state["inbox_load_error"] = True


def _clean(items):
    """Validate the parsed JSON into a list of well-formed email dicts."""
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
        reply = str(reply).strip() if reply else None
        sender = str(item.get("from") or "").strip() or "Unknown sender"
        subject = str(item.get("subject") or "").strip() or "(no subject)"
        cleaned.append({
            "from": sender,
            "subject": subject,
            "category": category,
            "one_line_summary": str(item.get("one_line_summary", "")).strip(),
            "suggested_reply": reply if category != "FYI" else None,
        })
    return cleaned


def _triage(text: str, demo: bool):
    """Run the triage and stash results in session state."""
    start = time.perf_counter()
    if demo:
        try:
            with st.spinner("Loading cached demo triage..."):
                raw = json.loads(CACHE_JSON.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            st.error("Demo cache is missing or corrupted (cache/inbox_sample.json). "
                     "Turn Demo Mode off or restore the file.")
            return
    else:
        n = len([p for p in text.split("---") if p.strip()])
        try:
            with st.spinner(f"Triaging {n} emails with Gemini (one call)..."):
                raw = llm.ask_claude_json(TRIAGE_SYSTEM, text,
                                          max_tokens=min(500 + 350 * n, 8000))
        except llm.LLMError as exc:
            st.error(str(exc))
            return
    emails = _clean(raw)
    if not emails:
        st.error("Could not extract any emails from the response. "
                 "Check that the emails are separated with --- and try again.")
        return
    st.session_state["inbox_result"] = {
        "emails": emails, "elapsed": time.perf_counter() - start,
    }


def _card(email: dict):
    with st.container(border=True):
        st.markdown(f"**{email['subject']}**")
        st.caption(f"From: {email['from']}")
        st.write(email["one_line_summary"])
        if email["suggested_reply"]:
            with st.expander("Suggested reply"):
                st.code(email["suggested_reply"], language=None)


def _show(result: dict):
    emails, elapsed = result["emails"], result["elapsed"]
    replies = sum(1 for e in emails if e["suggested_reply"])
    st.markdown("<div class='of-section-label'>Triaged inbox</div>", unsafe_allow_html=True)
    st.success(f"{len(emails)} emails triaged and {replies} replies drafted "
               f"in {elapsed:.1f} seconds.")
    columns = st.columns(len(CATEGORIES))
    for col, category in zip(columns, CATEGORIES):
        with col:
            bucket = [e for e in emails if e["category"] == category]
            st.markdown(f"### {STYLES[category]} · {len(bucket)}")
            if not bucket:
                st.caption("No emails in this category.")
            for email in bucket:
                _card(email)


def render():
    st.markdown(
        "<div class='of-module-head'><div class='of-topline'>Module 02</div>"
        "<h1>Inbox Triage</h1><p>Paste raw emails and get priority buckets with draft replies.</p></div>",
        unsafe_allow_html=True,
    )
    demo = bool(st.session_state.get("demo_mode"))

    with st.container(border=True):
        st.markdown("<div class='of-section-label'>Input</div>", unsafe_allow_html=True)
        st.text_area("Paste raw emails (separate with ---)", key="inbox_text", height=220)
        st.button("Load sample emails", on_click=_load_sample)
        if st.button("Triage Inbox", type="primary"):
            text = st.session_state.get("inbox_text", "")
            if not text.strip():
                st.warning("Please paste some emails first (or click 'Load sample emails').")
            else:
                _triage(text, demo)
    if st.session_state.pop("inbox_load_error", False):
        st.error("Sample file not found (samples/emails.txt).")

    result = st.session_state.get("inbox_result")
    if result:
        _show(result)
