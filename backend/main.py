"""FastAPI entry point for the full-stack OfficeFlow app."""
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend import config
from backend.errors import AppError, install_error_handlers
from backend.files import serve_file
from backend.services import ask_service, docs_service, inbox_service, minutes_service

app = FastAPI(title="OfficeFlow API")
MAX_AUDIO_BYTES = 50 * 1024 * 1024
MAX_CSV_BYTES = 2 * 1024 * 1024
MAX_PDF_BYTES = 20 * 1024 * 1024

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
install_error_handlers(app)


class InboxRequest(BaseModel):
    text: str = ""
    demo: bool = True


class AskRequest(BaseModel):
    doc_id: str | None = None
    question: str = ""
    demo: bool = True


async def read_limited(upload: UploadFile, max_bytes: int, label: str) -> bytes:
    data = await upload.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise AppError(f"{label} is too large. Please choose a smaller file.", 413)
    return data


@app.get("/api/health")
def health():
    return {
        "ok": True,
        "demo_default": config.demo_default(),
        "providers_available": config.providers_available(),
        "app_name": config.APP_NAME,
    }


@app.get("/api/files/{file_id}")
def files(file_id: str):
    return serve_file(file_id)


@app.post("/api/minutes")
async def minutes(
    audio: UploadFile | None = File(None),
    use_sample: bool = Form(False),
    demo: bool = Form(True),
):
    filename = audio.filename if audio is not None else None
    audio_bytes = await read_limited(audio, MAX_AUDIO_BYTES, "Audio file") if audio is not None else None
    return minutes_service.run(audio_bytes, filename, use_sample, demo)


@app.post("/api/inbox")
def inbox(payload: InboxRequest):
    return inbox_service.triage(payload.text, payload.demo)


@app.post("/api/docs")
async def docs(
    csv: UploadFile | None = File(None),
    doc_type: str = Form("Merit Certificate"),
    use_sample: bool = Form(False),
    demo: bool = Form(True),
):
    filename = csv.filename if csv is not None else None
    csv_bytes = await read_limited(csv, MAX_CSV_BYTES, "CSV file") if csv is not None else None
    return docs_service.run(csv_bytes, filename, doc_type, use_sample, demo)


@app.post("/api/ask/load")
async def ask_load(pdf: UploadFile = File(...)):
    return ask_service.load_pdf(await read_limited(pdf, MAX_PDF_BYTES, "PDF file"), pdf.filename)


@app.post("/api/ask/question")
def ask_question(payload: AskRequest):
    return ask_service.ask_question(payload.doc_id, payload.question, payload.demo)
