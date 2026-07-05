"""Module 1: Meeting Minutes — audio → transcript → structured minutes → Word doc."""
import json
import tempfile
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from lib import docgen, llm, transcribe

SAMPLE_AUDIO = Path("samples/meeting_sample.wav")
CACHE_JSON = Path("cache/minutes_sample.json")
OUTPUT_DIR = Path("outputs")
ALLOWED_AUDIO = {".mp3", ".wav", ".m4a"}

EXTRACT_SYSTEM = """You extract meeting minutes from a raw meeting transcript.
Return JSON with exactly these keys:
{"title": str, "date": str, "attendees": [str],
 "summary": [str], "action_items": [{"task": str, "owner": str, "deadline": str}],
 "decisions": [str]}
"summary" must be 3-5 short bullet points.
Extract only what is actually stated in the transcript. Use "Not specified" for
any field that is missing. Never invent names, dates, or deadlines."""


def _load_cache():
    """Demo mode: return the pre-generated minutes from cache/ (no API needed)."""
    try:
        with st.spinner("Loading cached demo output..."):
            return json.loads(CACHE_JSON.read_text(encoding="utf-8"))
    except FileNotFoundError:
        st.error("Demo cache is missing (cache/minutes_sample.json). Turn Demo Mode off or restore the file.")
    except json.JSONDecodeError:
        st.error("Demo cache file is corrupted. Restore cache/minutes_sample.json.")
    return None


def _generate(audio_path: Path):
    """Real pipeline: transcribe the audio, then extract structured minutes."""
    try:
        with st.spinner("Transcribing audio... (first run loads the Whisper model)"):
            transcript = transcribe.transcribe(audio_path)
    except Exception:
        st.error("Could not transcribe this file. Make sure it is a valid mp3, wav or m4a recording.")
        return None
    if not transcript:
        st.error("No speech was detected in the audio file.")
        return None
    try:
        with st.spinner("Extracting minutes with Gemini..."):
            data = llm.ask_claude_json(EXTRACT_SYSTEM, transcript, 2000)
    except llm.LLMError as exc:
        st.error(str(exc))
        return None
    if not isinstance(data, dict):
        st.error("Gemini returned an unexpected format. Please try again.")
        return None
    return data


def _make_docx(data: dict):
    """Write the Word document into outputs/ and return its bytes + filename."""
    try:
        with st.spinner("Generating Word document..."):
            OUTPUT_DIR.mkdir(exist_ok=True)
            out_path = OUTPUT_DIR / f"minutes_{datetime.now():%Y%m%d_%H%M%S}.docx"
            docgen.minutes_docx(data, out_path)
            return out_path.read_bytes(), out_path.name
    except Exception:
        st.error("Could not create the Word document. Check that outputs/ is writable.")
        return None


def _run(audio_path, demo: bool):
    """Full flow for one click: get data, build docx, store result for rendering."""
    start = time.perf_counter()
    data = _load_cache() if demo else _generate(audio_path)
    if data is None:
        return
    made = _make_docx(data)
    if made is None:
        return
    docx_bytes, docx_name = made
    st.session_state["minutes_result"] = {
        "data": data,
        "docx_bytes": docx_bytes,
        "docx_name": docx_name,
        "elapsed": time.perf_counter() - start,
    }


def _show(result: dict):
    data = result["data"]
    st.markdown("<div class='of-section-label'>Generated minutes</div>", unsafe_allow_html=True)
    result_box = st.container(border=True)
    with result_box:
        st.subheader(str(data.get("title", "Meeting Minutes")))
        attendees = ", ".join(str(a) for a in data.get("attendees") or []) or "Not specified"
        st.caption(f"Date: {data.get('date', 'Not specified')}  ·  Attendees: {attendees}")

        st.markdown("#### Summary")
        for bullet in data.get("summary") or ["No summary available."]:
            st.markdown(f"- {bullet}")

        st.markdown("#### Decisions")
        decisions = data.get("decisions") or []
        if decisions:
            for decision in decisions:
                st.markdown(f"- {decision}")
        else:
            st.markdown("_No decisions recorded._")

        st.markdown("#### Action Items")
        items = data.get("action_items") or []
        if items:
            table = pd.DataFrame(
                [{"Task": i.get("task", ""), "Owner": i.get("owner", ""),
                  "Deadline": i.get("deadline", "")} for i in items if isinstance(i, dict)]
            )
            st.dataframe(table, hide_index=True, width="stretch")
        else:
            st.markdown("_No action items recorded._")

        st.success(f"Done in {result['elapsed']:.1f} seconds — manual equivalent: ~30 minutes.")
        st.download_button(
            "Download Word document",
            result["docx_bytes"],
            file_name=result["docx_name"],
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )


def render():
    st.markdown(
        "<div class='of-module-head'><div class='of-topline'>Module 01</div>"
        "<h1>Meeting Minutes</h1><p>Upload audio and generate structured Word minutes.</p></div>",
        unsafe_allow_html=True,
    )
    demo = bool(st.session_state.get("demo_mode"))
    if demo:
        st.caption(
            "Meeting Minutes uses cached demo output on Streamlit Community Cloud so Whisper does not load on the free tier."
        )

    with st.container(border=True):
        st.markdown("<div class='of-section-label'>Input</div>", unsafe_allow_html=True)
        uploaded = st.file_uploader("Meeting audio", type=["mp3", "wav", "m4a"])
        col1, col2 = st.columns(2)
        generate_clicked = col1.button("Generate Minutes", type="primary")
        sample_clicked = col2.button("Use sample audio")

    if generate_clicked:
        if demo:
            _run(None, demo=True)
        elif uploaded is None:
            st.warning("Please upload an audio file first (mp3, wav or m4a).")
        else:
            suffix = Path(uploaded.name).suffix or ".mp3"
            if suffix.lower() not in ALLOWED_AUDIO:
                st.error("Please upload an audio file in mp3, wav or m4a format.")
                return
            audio_bytes = uploaded.getbuffer()
            if not audio_bytes:
                st.error("The uploaded audio file is empty. Please choose a recording with speech.")
                return
            tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
            try:
                tmp.write(audio_bytes)
                tmp.close()
                _run(Path(tmp.name), demo=False)
            finally:
                Path(tmp.name).unlink(missing_ok=True)
    elif sample_clicked:
        if demo:
            _run(None, demo=True)
        elif not SAMPLE_AUDIO.exists():
            st.error("Sample audio is missing (samples/meeting_sample.wav). Add it or use Demo Mode.")
        else:
            _run(SAMPLE_AUDIO, demo=False)

    result = st.session_state.get("minutes_result")
    if result:
        _show(result)
