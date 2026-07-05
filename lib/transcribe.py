"""faster-whisper wrapper. The model is loaded once, lazily, so repeat runs are fast."""

_model = None


def _get_model():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel

        _model = WhisperModel("small", device="cpu", compute_type="int8")
    return _model


def transcribe(audio_path) -> str:
    """Transcribe an audio file and return the full text."""
    segments, _info = _get_model().transcribe(str(audio_path))
    return " ".join(segment.text.strip() for segment in segments).strip()
