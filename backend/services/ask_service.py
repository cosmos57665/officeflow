"""PDF Q&A workflow for the FastAPI backend."""
import json
import time
from pathlib import Path
from uuid import uuid4

import fitz

from backend.errors import AppError
from lib import llm

CACHE_JSON = Path("cache/ask_sample.json")
MAX_CONTEXT_CHARS = 80_000
_DOCS: dict[str, list[dict]] = {}

ASK_SYSTEM = """You answer questions about an uploaded office PDF.
Answer ONLY from the document.
Cite page numbers like (p. 4) after each claim.
When the answer is absent, reply exactly: This is not covered in the document."""


def _extract_pages(pdf_bytes: bytes):
    pages = []
    try:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            for index, page in enumerate(doc, start=1):
                pages.append({"page": index, "text": page.get_text("text").strip()})
    except Exception as exc:
        raise AppError("Could not read this PDF. Upload a valid text-based PDF.") from exc
    if not pages or not any(page["text"] for page in pages):
        raise AppError("No readable text was found in this PDF.")
    return pages


def _context(pages) -> str:
    parts = [f"[Page {p['page']}]\n{p['text']}" for p in pages if p["text"]]
    return "\n\n".join(parts)[:MAX_CONTEXT_CHARS]


def load_pdf(pdf_bytes: bytes, filename: str):
    if Path(filename).suffix.lower() != ".pdf":
        raise AppError("Please upload a PDF file.")
    pages = _extract_pages(pdf_bytes)
    doc_id = uuid4().hex
    _DOCS[doc_id] = pages
    chars = sum(len(p["text"]) for p in pages)
    result = {
        "doc_id": doc_id,
        "pages": len(pages),
        "words": sum(len(p["text"].split()) for p in pages),
    }
    if chars > MAX_CONTEXT_CHARS:
        result["warning"] = "This PDF is long. Only the first 80k characters will be used."
    return result


def _demo_answer(question: str):
    try:
        answers = json.loads(CACHE_JSON.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AppError("Demo cache is missing (cache/ask_sample.json).") from exc
    except json.JSONDecodeError as exc:
        raise AppError("Demo cache file is corrupted (cache/ask_sample.json).") from exc
    needle = question.lower().strip()
    for sample, answer in answers.items():
        sample_lower = str(sample).lower().strip()
        if sample_lower in needle or needle in sample_lower:
            return str(answer)
    samples = ", ".join(str(sample) for sample in answers.keys())
    return f"Demo Mode can answer only these sample questions: {samples}"


def ask_question(doc_id: str | None, question: str, demo: bool):
    start = time.perf_counter()
    if not question.strip():
        raise AppError("Please type a question first.")
    provider = "demo"
    if demo:
        answer = _demo_answer(question)
    else:
        pages = _DOCS.get(doc_id or "")
        if not pages:
            raise AppError("Please upload a PDF first.")
        user = f"Document:\n{_context(pages)}\n\nQuestion: {question}"
        try:
            answer, provider = llm.ask_claude_with_provider(ASK_SYSTEM, user, 1200)
        except llm.LLMError as exc:
            raise AppError(str(exc), 503) from exc
    return {"answer": answer, "elapsed": time.perf_counter() - start, "provider": provider}
