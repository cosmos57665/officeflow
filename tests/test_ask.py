import unittest
from contextlib import nullcontext
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

from fpdf import FPDF

from modules import ask


class AskPdfTests(unittest.TestCase):
    def test_extract_pages_returns_one_based_page_text(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.pdf"
            pdf = FPDF()
            for text in ("First page policy text", "Second page reimbursement text"):
                pdf.add_page()
                pdf.set_font("Helvetica", size=12)
                pdf.multi_cell(0, 10, text)
            pdf.output(path)

            pages = ask._extract_pages(path.read_bytes())

        self.assertEqual(
            pages,
            [
                {"page": 1, "text": "First page policy text"},
                {"page": 2, "text": "Second page reimbursement text"},
            ],
        )

    def test_build_document_context_trims_after_80k_characters(self):
        pages = [
            {"page": 1, "text": "A" * 50_000},
            {"page": 2, "text": "B" * 50_000},
        ]

        context = ask._build_document_context(pages)

        self.assertLessEqual(len(context), ask.MAX_CONTEXT_CHARS)
        self.assertIn("[Page 1]", context)
        self.assertIn("[Page 2]", context)


class AskDemoTests(unittest.TestCase):
    def test_find_demo_answer_matches_lowercase_substring(self):
        answers = {
            "annual leave": "Annual leave answer.",
            "reimbursement deadline": "Reimbursement answer.",
        }

        answer = ask._find_demo_answer("What is the ANNUAL leave rule?", answers)

        self.assertEqual(answer, "Annual leave answer.")

    def test_find_demo_answer_returns_none_for_unmatched_question(self):
        answers = {"annual leave": "Annual leave answer."}

        self.assertIsNone(ask._find_demo_answer("Who approves travel?", answers))

    def test_demo_question_uses_cache_without_loaded_pdf(self):
        session_state = {}
        with TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "ask_sample.json"
            cache_path.write_text('{"annual leave": "Annual leave answer."}', encoding="utf-8")
            with patch.object(ask, "CACHE_JSON", cache_path), patch.multiple(
                ask.st,
                session_state=session_state,
                spinner=Mock(return_value=nullcontext()),
                error=Mock(),
                info=Mock(),
            ):
                ask._ask_document("What is the annual leave policy?", demo=True)

        self.assertEqual(session_state["ask_chat"][0]["answer"], "Annual leave answer.")
        self.assertIn("elapsed", session_state["ask_chat"][0])


if __name__ == "__main__":
    unittest.main()
