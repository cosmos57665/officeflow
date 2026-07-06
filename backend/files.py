"""Generated-file registry and serving helpers."""
import base64
from pathlib import Path

from fastapi.responses import FileResponse

from backend.errors import AppError

OUTPUT_DIR = Path("outputs")


def register_file(path: Path) -> str:
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(OUTPUT_DIR.resolve())
    except ValueError as exc:
        raise AppError("Generated file is outside the outputs folder.", 500) from exc
    token = base64.urlsafe_b64encode(relative.as_posix().encode("utf-8")).decode("ascii")
    return token.rstrip("=")


def serve_file(file_id: str) -> FileResponse:
    try:
        padded = file_id + "=" * (-len(file_id) % 4)
        relative_text = base64.urlsafe_b64decode(padded.encode("ascii")).decode("utf-8")
    except Exception as exc:
        raise AppError("This generated file is no longer available.", 404) from exc
    path = (OUTPUT_DIR / relative_text).resolve()
    try:
        path.relative_to(OUTPUT_DIR.resolve())
    except ValueError as exc:
        raise AppError("This generated file is no longer available.", 404) from exc
    if not path.exists() or not path.is_file():
        raise AppError("This generated file is no longer available.", 404)
    return FileResponse(path, filename=path.name)
