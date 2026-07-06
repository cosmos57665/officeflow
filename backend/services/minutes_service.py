"""Meeting minutes workflow for the FastAPI backend."""
import json
import tempfile
import time
from datetime import datetime
from pathlib import Path

from backend.errors import AppError
from backend.files import register_file
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


def _cache():
    try:
        return json.loads(CACHE_JSON.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AppError("Demo cache is missing (cache/minutes_sample.json).") from exc
    except json.JSONDecodeError as exc:
        raise AppError("Demo cache file is corrupted (cache/minutes_sample.json).") from exc


def _generate(audio_path: Path):
    try:
        transcript = transcribe.transcribe(audio_path)
    except transcribe.TranscriptionError as exc:
        raise AppError(str(exc), 503) from exc
    except Exception as exc:
        raise AppError("Could not transcribe this audio file.") from exc
    if not transcript:
        raise AppError("No speech was detected in the audio file.")
    try:
        data, provider = llm.ask_claude_json_with_provider(EXTRACT_SYSTEM, transcript, 2000)
    except llm.LLMError as exc:
        raise AppError(str(exc), 503) from exc
    if not isinstance(data, dict):
        raise AppError("The AI returned an unexpected minutes format.")
    return data, provider


def _make_docx(data: dict) -> str:
    try:
        OUTPUT_DIR.mkdir(exist_ok=True)
        out_path = OUTPUT_DIR / f"minutes_{datetime.now():%Y%m%d_%H%M%S}.docx"
        docgen.minutes_docx(data, out_path)
        return register_file(out_path)
    except Exception as exc:
        raise AppError("Could not create the Word document.", 500) from exc


def _string_list(value, fallback: str) -> list[str]:
    if isinstance(value, list):
        cleaned = [str(item).strip() for item in value if str(item).strip()]
        return cleaned or [fallback]
    if value:
        return [str(value).strip()]
    return [fallback]


def _action_items(value) -> list[dict]:
    if not isinstance(value, list):
        return []
    cleaned = []
    for item in value:
        if not isinstance(item, dict):
            continue
        cleaned.append({
            "task": str(item.get("task") or "").strip() or "Not specified",
            "owner": str(item.get("owner") or "").strip() or "Not specified",
            "deadline": str(item.get("deadline") or "").strip() or "Not specified",
        })
    return cleaned


def _clean_minutes(data: dict) -> dict:
    return {
        "title": str(data.get("title") or "Meeting Minutes").strip(),
        "date": str(data.get("date") or "Not specified").strip(),
        "attendees": _string_list(data.get("attendees"), "Not specified"),
        "summary": _string_list(data.get("summary"), "No summary available."),
        "decisions": _string_list(data.get("decisions"), "No decisions recorded."),
        "action_items": _action_items(data.get("action_items")),
    }


def run(audio_bytes: bytes | None, filename: str | None, use_sample: bool, demo: bool):
    start = time.perf_counter()
    provider = "demo"
    if demo:
        data = _cache()
    else:
        if use_sample:
            if not SAMPLE_AUDIO.exists():
                raise AppError("Sample audio is missing (samples/meeting_sample.wav).")
            data, provider = _generate(SAMPLE_AUDIO)
        else:
            suffix = Path(filename or "").suffix.lower()
            if suffix not in ALLOWED_AUDIO:
                raise AppError("Please upload an audio file in mp3, wav or m4a format.")
            if not audio_bytes:
                raise AppError("The uploaded audio file is empty.")
            tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
            try:
                tmp.write(audio_bytes)
                tmp.close()
                data, provider = _generate(Path(tmp.name))
            finally:
                Path(tmp.name).unlink(missing_ok=True)
    data = _clean_minutes(data)
    return {
        "data": data,
        "elapsed": time.perf_counter() - start,
        "provider": provider,
        "docx_file_id": _make_docx(data),
    }
