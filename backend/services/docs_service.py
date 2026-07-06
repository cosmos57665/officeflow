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
ALIASES = {
    "name": ["name", "student", "student_name", "employee", "employee_name", "full_name"],
    "class": ["class", "grade", "department", "team", "role", "designation"],
    "marks": ["marks", "score", "performance_score", "rating", "progress", "percent", "percentage"],
    "achievement": [
        "achievement", "achievements", "remark", "remarks", "feedback", "comments",
        "comment", "summary", "progress_note", "progress_notes", "strengths",
    ],
}

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
    original_columns = [str(c).strip() for c in df.columns]
    normalized_columns = [c.lower().replace(" ", "_").replace("-", "_") for c in original_columns]
    df.columns = normalized_columns
    df = _normalize_columns(df)
    df = df.dropna(subset=["name"]).reset_index(drop=True)
    if df.empty:
        raise AppError("The CSV has no usable rows.")
    return df


def _first_existing(df, aliases):
    for alias in aliases:
        if alias in df.columns:
            return alias
    return None


def _normalize_columns(df):
    normalized = pd.DataFrame()
    name_col = _first_existing(df, ALIASES["name"])
    if not name_col:
        raise AppError(
            "CSV is missing a name column. Use name, employee_name, student_name, or full_name."
        )
    normalized["name"] = df[name_col].astype(str).str.strip()

    class_col = _first_existing(df, ALIASES["class"])
    marks_col = _first_existing(df, ALIASES["marks"])
    achievement_col = _first_existing(df, ALIASES["achievement"])

    normalized["class"] = (
        df[class_col].astype(str).str.strip() if class_col else "General"
    )
    normalized["marks"] = (
        df[marks_col].astype(str).str.strip() if marks_col else "Not specified"
    )
    if achievement_col:
        normalized["achievement"] = df[achievement_col].astype(str).str.strip()
    else:
        used = {name_col, class_col, marks_col}
        extra_cols = [c for c in df.columns if c not in used and c is not None]
        if not extra_cols:
            raise AppError(
                "CSV needs progress details. Add achievement, remarks, feedback, comments, or similar."
            )
        normalized["achievement"] = df[extra_cols].apply(
            lambda row: "; ".join(
                f"{col.replace('_', ' ')}: {value}"
                for col, value in row.items()
                if str(value).strip() and str(value).lower() != "nan"
            ) or "Progress details not specified.",
            axis=1,
        )
    return normalized


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
        if doc_type == "Progress Report":
            docgen.progress_report_pdf(
                str(row["name"]),
                str(row["class"]),
                str(row["marks"]),
                str(row["achievement"]),
                remarks[row["name"]],
                path,
            )
        else:
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
