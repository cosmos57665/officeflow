from pathlib import Path
from tempfile import TemporaryDirectory

import fitz

from lib import docgen


def _pdf_text(path: Path) -> str:
    with fitz.open(path) as pdf:
        return "\n".join(page.get_text("text") for page in pdf)


def test_progress_report_pdf_uses_report_layout_not_certificate_copy():
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "progress.pdf"
        docgen.progress_report_pdf(
            "Asha Rao",
            "Operations",
            "92",
            "Handled filing and improved turnaround time.",
            "Asha is making steady progress.",
            path,
        )

        text = _pdf_text(path)

    assert "Progress Summary" in text
    assert "Department / Class" in text
    assert "Performance Score" in text
    assert "Manager / Teacher Remarks" in text
    assert "This progress report is issued to" not in text
    assert "Signature" not in text
