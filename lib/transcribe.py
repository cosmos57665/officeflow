"""Speech-to-text wrapper with Groq cloud first and local Whisper fallback."""
import os
import threading
from pathlib import Path

import httpx
from dotenv import load_dotenv

_model = None
_model_lock = threading.Lock()
_preload_thread = None
_preload_started = False
GROQ_TRANSCRIBE_MODEL = "whisper-large-v3-turbo"
GROQ_TRANSCRIBE_URL = "https://api.groq.com/openai/v1/audio/transcriptions"


def _get_model(local_files_only: bool = False):
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                from faster_whisper import WhisperModel

                _model = WhisperModel(
                    "small",
                    device="cpu",
                    compute_type="int8",
                    local_files_only=local_files_only,
                )
    return _model


def _preload_worker():
    try:
        _get_model(local_files_only=True)
    except Exception:
        pass


def preload_model_background():
    """Start one daemon thread to warm the Whisper model without blocking app startup."""
    global _preload_started, _preload_thread
    if _model is not None:
        return None
    if _preload_thread is not None and _preload_thread.is_alive():
        return _preload_thread
    if _preload_started:
        return _preload_thread
    _preload_started = True
    _preload_thread = threading.Thread(
        target=_preload_worker,
        name="officeflow-whisper-preload",
        daemon=True,
    )
    _preload_thread.start()
    return _preload_thread


def _groq_key() -> str | None:
    load_dotenv()
    return os.getenv("GROQ_API_KEY")


def _transcribe_local(audio_path) -> str:
    segments, _info = _get_model().transcribe(str(audio_path))
    return " ".join(segment.text.strip() for segment in segments).strip()


def _transcribe_groq(audio_path) -> str:
    key = _groq_key()
    if not key:
        raise RuntimeError("GROQ_API_KEY is not configured.")
    path = Path(audio_path)
    with path.open("rb") as audio:
        response = httpx.post(
            GROQ_TRANSCRIBE_URL,
            headers={"Authorization": f"Bearer {key}"},
            data={"model": GROQ_TRANSCRIBE_MODEL, "response_format": "json"},
            files={"file": (path.name, audio, "application/octet-stream")},
            timeout=180,
        )
    response.raise_for_status()
    text = response.json().get("text", "")
    if not str(text).strip():
        raise RuntimeError("Groq returned an empty transcript.")
    return str(text).strip()


def transcribe(audio_path) -> str:
    """Transcribe an audio file and return the full text.

    Groq is tried first when GROQ_API_KEY is configured because it is much
    faster for long meetings. Local faster-whisper remains the offline fallback.
    """
    if _groq_key():
        try:
            return _transcribe_groq(audio_path)
        except Exception:
            pass
    return _transcribe_local(audio_path)
