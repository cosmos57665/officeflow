"""Module 4: Ask — upload a PDF and ask cited questions about it."""
import json
import time
from pathlib import Path

import fitz  # PyMuPDF
import streamlit as st

from lib import llm

CACHE_JSON = Path("cache/ask_sample.json")
MAX_CONTEXT_CHARS = 80_000

ASK_SYSTEM = """You answer questions about an uploaded office PDF.
Answer ONLY from the document.
Cite page numbers like (p. 4) after each claim.
When the answer is absent, reply exactly: This is not covered in the document."""


def _extract_pages(pdf_bytes: bytes):
    """Return one dict per PDF page with 1-based page numbers and extracted text."""
    pages = []
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for index, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            pages.append({"page": index, "text": text})
    return pages


def _word_count(pages) -> int:
    return sum(len(page["text"].split()) for page in pages)


def _total_chars(pages) -> int:
    return sum(len(page["text"]) for page in pages)


def _build_document_context(pages) -> str:
    parts = [f"[Page {page['page']}]\n{page['text']}" for page in pages if page["text"]]
    return "\n\n".join(parts)[:MAX_CONTEXT_CHARS]


def _find_demo_answer(question: str, answers: dict):
    needle = question.lower().strip()
    for sample, answer in answers.items():
        sample_lower = str(sample).lower().strip()
        if sample_lower in needle or needle in sample_lower:
            return str(answer)
    return None


def _load_demo_answers():
    try:
        with st.spinner("Loading cached demo answers..."):
            data = json.loads(CACHE_JSON.read_text(encoding="utf-8"))
    except FileNotFoundError:
        st.error("Demo cache is missing (cache/ask_sample.json). Turn Demo Mode off or restore the file.")
        return None
    except json.JSONDecodeError:
        st.error("Demo cache file is corrupted. Restore cache/ask_sample.json.")
        return None
    if not isinstance(data, dict) or not data:
        st.error("Demo cache has no sample questions. Restore cache/ask_sample.json.")
        return None
    return data


def _load_pdf(uploaded):
    if Path(uploaded.name).suffix.lower() != ".pdf":
        st.error("Please upload a PDF file.")
        return
    try:
        with st.spinner("Reading PDF pages..."):
            pages = _extract_pages(uploaded.getvalue())
    except Exception:
        st.error("Could not read this PDF. Please upload a valid, text-based PDF file.")
        return
    if not pages or not any(page["text"] for page in pages):
        st.error("No readable text was found in this PDF.")
        return
    st.session_state["ask_pages"] = pages
    st.session_state["ask_pdf_name"] = uploaded.name
    st.session_state["ask_chat"] = []


def _ask_document(question: str, demo: bool):
    start = time.perf_counter()
    if demo:
        answers = _load_demo_answers()
        if answers is None:
            return
        answer = _find_demo_answer(question, answers)
        if answer is None:
            samples = "\n".join(f"- {sample}" for sample in answers.keys())
            st.info("Demo Mode: use one of these sample questions:\n" + samples)
            answer = "Demo Mode can answer only the listed sample questions."
    else:
        pages = st.session_state.get("ask_pages", [])
        context = _build_document_context(pages)
        user = f"Document:\n{context}\n\nQuestion: {question}"
        try:
            with st.spinner("Searching the document with Claude..."):
                answer = llm.ask_claude(ASK_SYSTEM, user, max_tokens=1200)
        except llm.LLMError as exc:
            st.error(str(exc))
            return
    st.session_state.setdefault("ask_chat", []).append(
        {"question": question, "answer": answer, "elapsed": time.perf_counter() - start}
    )


def _show_loaded(pages):
    chars = _total_chars(pages)
    st.success(f"Loaded: {len(pages)} pages, ~{_word_count(pages)} words.")
    if chars > MAX_CONTEXT_CHARS:
        st.warning("This PDF is long. Only the first 80k characters will be used for answers.")


def _render_history():
    for item in st.session_state.get("ask_chat", []):
        with st.chat_message("user"):
            st.write(item["question"])
        with st.chat_message("assistant"):
            st.write(item["answer"])
            st.caption(f"Answered in {item['elapsed']:.1f} seconds.")


def render():
    st.header("Ask PDF")
    st.caption("Upload a PDF, then ask questions that must be answered only from the document.")
    demo = bool(st.session_state.get("demo_mode"))

    uploaded = st.file_uploader("Policy or office PDF", type=["pdf"])
    if uploaded is not None and uploaded.name != st.session_state.get("ask_pdf_name"):
        _load_pdf(uploaded)

    pages = st.session_state.get("ask_pages", [])
    if pages:
        _show_loaded(pages)
    elif demo:
        st.caption("Demo Mode: ask a cached sample question without calling Claude.")
    else:
        st.info("Upload a PDF to begin.")

    _render_history()

    question = st.chat_input("Ask a question about the PDF")
    if question:
        question = question.strip()
        if not question:
            st.warning("Please type a question first.")
        elif not pages and not demo:
            st.warning("Please upload a PDF first.")
        else:
            st.session_state.setdefault("ask_chat", []).append(
                {"question": question, "answer": "", "elapsed": 0}
            )
            with st.chat_message("user"):
                st.write(question)
            st.session_state["ask_chat"].pop()
            _ask_document(question, demo)
            if st.session_state.get("ask_chat"):
                item = st.session_state["ask_chat"][-1]
                with st.chat_message("assistant"):
                    st.write(item["answer"])
                    st.caption(f"Answered in {item['elapsed']:.1f} seconds.")
