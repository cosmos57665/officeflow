"""Generated-file registry and serving helpers."""
from pathlib import Path
from uuid import uuid4

from fastapi.responses import FileResponse

from backend.errors import AppError

OUTPUT_DIR = Path("outputs")
_FILES: dict[str, Path] = {}


def register_file(path: Path) -> str:
    resolved = path.resolve()
    try:
        resolved.relative_to(OUTPUT_DIR.resolve())
    except ValueError as exc:
        raise AppError("Generated file is outside the outputs folder.", 500) from exc
    file_id = f"{uuid4().hex}{resolved.suffix.lower()}"
    _FILES[file_id] = resolved
    return file_id


def serve_file(file_id: str) -> FileResponse:
    path = _FILES.get(file_id)
    if path is None or not path.exists():
        raise AppError("This generated file is no longer available.", 404)
    return FileResponse(path, filename=path.name)
