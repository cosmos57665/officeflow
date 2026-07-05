import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

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


if __name__ == "__main__":
    unittest.main()
