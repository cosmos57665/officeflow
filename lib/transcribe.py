"""faster-whisper wrapper. The model is loaded once so repeat runs are fast."""
import threading

_model = None
_model_lock = threading.Lock()
_preload_thread = None
_preload_started = False


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


def transcribe(audio_path) -> str:
    """Transcribe an audio file and return the full text."""
    segments, _info = _get_model().transcribe(str(audio_path))
    return " ".join(segment.text.strip() for segment in segments).strip()
