"""Bulk document generation workflow for the FastAPI backend."""
import io
import json
import re
import time
import zipfile
from pathlib import Path
from uuid import uuid4

import fitz
import pandas as pd

from backend.errors import AppError
from backend.files import register_file
from lib import docgen, llm

SAMPLE_CSV = Path("samples/students.csv")
CACHE_JSON = Path("cache/remarks_sample.json")
OUTPUT_ROOT = Path("outputs/certificates")
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


def _read_csv(data: bytes, filename: str):
    if Path(filename).suffix.lower() != ".csv":
        raise AppError("Please upload a CSV file.")
    try:
        df = pd.read_csv(io.BytesIO(data))
    except Exception as exc:
        raise AppError("Could not read this file as a CSV.") from exc
    df.columns = [str(c).strip().lower() for c in df.columns]
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise AppError(f"CSV is missing required column(s): {', '.join(missing)}.")
    df = df.dropna(subset=["name"]).reset_index(drop=True)
    if df.empty:
        raise AppError("The CSV has no student rows.")
    return df


def _remarks(df, doc_type: str, demo: bool):
    provider = "demo"
    if demo:
        try:
            raw = json.loads(CACHE_JSON.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise AppError("Demo cache is missing (cache/remarks_sample.json).") from exc
        except json.JSONDecodeError as exc:
            raise AppError("Demo cache file is corrupted (cache/remarks_sample.json).") from exc
    else:
        rows = df[REQUIRED].to_dict(orient="records")
        try:
            raw, provider = llm.ask_claude_json_with_provider(
                REMARKS_SYSTEM.format(doc_type=doc_type),
                json.dumps(rows, ensure_ascii=False),
                max_tokens=min(400 + 120 * len(rows), 8000),
            )
        except llm.LLMError as exc:
            raise AppError(str(exc), 503) from exc
    by_name = {str(i.get("name", "")).strip(): str(i.get("remark", "")).strip()
               for i in raw if isinstance(i, dict)} if isinstance(raw, list) else {}
    return {row["name"]: by_name.get(str(row["name"]).strip())
            or f"Recognized for scoring {row['marks']} marks in class {row['class']}."
            for _, row in df.iterrows()}, provider


def _make_outputs(df, remarks: dict, doc_type: str):
    style = DOC_TYPES[doc_type]
    output_dir = OUTPUT_ROOT / uuid4().hex
    preview_dir = output_dir / "previews"
    output_dir.mkdir(parents=True, exist_ok=True)
    preview_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, row in df.iterrows():
        safe = re.sub(r"[^A-Za-z0-9]+", "_", str(row["name"])).strip("_") or "student"
        path = output_dir / f"{i + 1:02d}_{safe}.pdf"
        docgen.certificate_pdf(str(row["name"]), remarks[row["name"]], path,
                               title=style["title"], subtitle=style["subtitle"])
        paths.append(path)
    zip_path = output_dir / "certificates.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in paths:
            zf.write(path, arcname=path.name)
    previews = []
    for path in paths[:3]:
        img_path = preview_dir / f"{path.stem}.png"
        with fitz.open(path) as doc:
            img_path.write_bytes(doc.load_page(0).get_pixmap(dpi=80).tobytes("png"))
        previews.append({"name": path.name, "file_id": register_file(img_path)})
    return register_file(zip_path), previews


def run(csv_bytes: bytes | None, filename: str | None, doc_type: str,
        use_sample: bool, demo: bool):
    start = time.perf_counter()
    if doc_type not in DOC_TYPES:
        raise AppError("Please choose a valid document type.")
    if demo or use_sample:
        if not SAMPLE_CSV.exists():
            raise AppError("Sample CSV is missing (samples/students.csv).")
        df = _read_csv(SAMPLE_CSV.read_bytes(), SAMPLE_CSV.name)
    else:
        if not csv_bytes:
            raise AppError("Please upload a CSV file first.")
        df = _read_csv(csv_bytes, filename or "")
    remarks, provider = _remarks(df, doc_type, demo)
    try:
        zip_file_id, previews = _make_outputs(df, remarks, doc_type)
    except Exception as exc:
        raise AppError("Could not create the PDF files.", 500) from exc
    return {
        "count": len(df), "elapsed": time.perf_counter() - start,
        "provider": provider, "zip_file_id": zip_file_id, "previews": previews,
    }
