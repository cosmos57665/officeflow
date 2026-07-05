"""Module 3: Docs — CSV of students → batched Claude remarks → per-student PDFs → zip."""
import io
import json
import re
import time
import zipfile
from pathlib import Path

import fitz  # PyMuPDF
import pandas as pd
import streamlit as st

from lib import docgen, llm

SAMPLE_CSV = Path("samples/students.csv")
CACHE_JSON = Path("cache/remarks_sample.json")
OUTPUT_DIR = Path("outputs/certificates")
REQUIRED = ["name", "class", "marks", "achievement"]

DOC_TYPES = {
    "Merit Certificate": {"title": "Merit Certificate",
                          "subtitle": "This certificate is proudly presented to"},
    "Progress Report": {"title": "Progress Report",
                        "subtitle": "This progress report is issued to"},
}

REMARKS_SYSTEM = """You write short remarks for school documents ({doc_type}).
Given a JSON list of students with name, class, marks (out of 100) and achievement,
return a JSON array with one object per student, in the same order:
[{{"name": str, "remark": str}}]
Each remark must be 1-2 sentences, personalized, professional and encouraging,
grounded only in that student's marks and achievement. Never invent facts."""


def _read_csv(uploaded):
    """Parse and validate the uploaded CSV. Returns a DataFrame or None."""
    if Path(getattr(uploaded, "name", "")).suffix.lower() != ".csv":
        st.error("Please upload a CSV file.")
        return None
    try:
        df = pd.read_csv(uploaded)
    except Exception:
        st.error("Could not read this file as a CSV. Please upload a valid .csv file.")
        return None
    df.columns = [str(c).strip().lower() for c in df.columns]
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        st.error(f"CSV is missing required column(s): {', '.join(missing)}. "
                 f"Expected columns: {', '.join(REQUIRED)}.")
        return None
    df = df.dropna(subset=["name"]).reset_index(drop=True)
    if df.empty:
        st.error("The CSV has no student rows. Add at least one student and try again.")
        return None
    return df


def _fallback_remark(row) -> str:
    return (f"Recognized for scoring {row['marks']} marks in class {row['class']} "
            f"and for the achievement: {row['achievement']}.")


def _get_remarks(df, doc_type: str, demo: bool):
    """Return {name: remark} for every row, or None on failure."""
    if demo:
        try:
            with st.spinner("Loading cached demo remarks..."):
                cached = json.loads(CACHE_JSON.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            st.error("Demo cache is missing or corrupted (cache/remarks_sample.json). "
                     "Turn Demo Mode off or restore the file.")
            return None
    else:
        rows = df[REQUIRED].to_dict(orient="records")
        try:
            with st.spinner(f"Writing {len(rows)} personalized remarks with Claude (one batched call)..."):
                cached = llm.ask_claude_json(
                    REMARKS_SYSTEM.format(doc_type=doc_type),
                    json.dumps(rows, ensure_ascii=False),
                    max_tokens=min(400 + 120 * len(rows), 8000),
                )
        except llm.LLMError as exc:
            st.error(str(exc))
            return None
    by_name = {str(item.get("name", "")).strip(): str(item.get("remark", "")).strip()
               for item in cached if isinstance(item, dict)} if isinstance(cached, list) else {}
    return {row["name"]: by_name.get(str(row["name"]).strip()) or _fallback_remark(row)
            for _, row in df.iterrows()}


def _make_pdfs(df, remarks: dict, doc_type: str):
    """Write one PDF per student into outputs/certificates/. Returns list of paths."""
    style = DOC_TYPES[doc_type]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUTPUT_DIR.glob("*.pdf"):
        old.unlink()
    paths = []
    for i, row in df.iterrows():
        safe = re.sub(r"[^A-Za-z0-9]+", "_", str(row["name"])).strip("_") or "student"
        path = OUTPUT_DIR / f"{i + 1:02d}_{safe}.pdf"
        docgen.certificate_pdf(str(row["name"]), remarks[row["name"]], path,
                               title=style["title"], subtitle=style["subtitle"])
        paths.append(path)
    return paths


def _zip_bytes(paths) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in paths:
            zf.write(path, arcname=path.name)
    return buf.getvalue()


def _previews(paths, count=3):
    """Render first pages of the first few PDFs as PNG bytes via PyMuPDF."""
    images = []
    for path in paths[:count]:
        with fitz.open(path) as doc:
            images.append(doc.load_page(0).get_pixmap(dpi=80).tobytes("png"))
    return images


def _run(df, doc_type: str, demo: bool):
    start = time.perf_counter()
    remarks = _get_remarks(df, doc_type, demo)
    if remarks is None:
        return
    try:
        with st.spinner(f"Generating {len(df)} PDF documents..."):
            paths = _make_pdfs(df, remarks, doc_type)
            zipped = _zip_bytes(paths)
            images = _previews(paths)
    except Exception:
        st.error("Could not create the PDF files. Check that outputs/ is writable.")
        return
    st.session_state["docs_result"] = {
        "zip": zipped, "images": images, "count": len(paths),
        "names": [p.name for p in paths[:len(images)]],
        "doc_type": doc_type, "elapsed": time.perf_counter() - start,
    }


def _show(result: dict):
    n, elapsed = result["count"], result["elapsed"]
    st.markdown("<div class='of-section-label'>Generated documents</div>", unsafe_allow_html=True)
    st.success(f"Generated {n} documents in {elapsed:.1f} seconds — "
               f"manual equivalent: ~{n * 5} minutes.")
    st.download_button(f"Download all {n} PDFs (zip)", result["zip"],
                       file_name="certificates.zip", mime="application/zip")
    st.markdown("#### Sample previews")
    cols = st.columns(len(result["images"]))
    for col, img, name in zip(cols, result["images"], result["names"]):
        col.image(img, caption=name, width="stretch")


def render():
    st.markdown(
        "<div class='of-module-head'><div class='of-topline'>Module 03</div>"
        "<h1>Bulk Document Generator</h1><p>Upload a CSV and generate personalized PDFs in one run.</p></div>",
        unsafe_allow_html=True,
    )
    demo = bool(st.session_state.get("demo_mode"))

    with st.container(border=True):
        st.markdown("<div class='of-section-label'>Input</div>", unsafe_allow_html=True)
        uploaded = st.file_uploader("Student CSV (columns: name, class, marks, achievement)", type=["csv"])
        df = None
        if uploaded is not None:
            df = _read_csv(uploaded)
        elif demo and SAMPLE_CSV.exists():
            df = _read_csv(SAMPLE_CSV)
            if df is not None:
                st.caption("Demo Mode: using samples/students.csv")
        if df is not None:
            st.dataframe(df, hide_index=True, width="stretch")
        doc_type = st.selectbox("Document type", list(DOC_TYPES.keys()))

        if st.button("Generate All", type="primary"):
            if df is None:
                st.warning("Please upload a CSV file first.")
            else:
                _run(df, doc_type, demo)

    result = st.session_state.get("docs_result")
    if result:
        _show(result)
