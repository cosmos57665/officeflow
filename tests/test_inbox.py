import unittest
from contextlib import nullcontext
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

from modules import inbox


class InboxCleanTests(unittest.TestCase):
    def test_blank_fields_get_safe_display_defaults(self):
        cleaned = inbox._clean([
            {
                "from": "   ",
                "subject": "",
                "category": "Unexpected",
                "one_line_summary": "  Needs review. ",
                "suggested_reply": "  Reply draft. ",
            }
        ])

        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned[0]["from"], "Unknown sender")
        self.assertEqual(cleaned[0]["subject"], "(no subject)")
        self.assertEqual(cleaned[0]["category"], "FYI")
        self.assertEqual(cleaned[0]["one_line_summary"], "Needs review.")
        self.assertIsNone(cleaned[0]["suggested_reply"])


class InboxTriageTests(unittest.TestCase):
    def setUp(self):
        self.session_state = {}
        self.st_patcher = patch.multiple(
            inbox.st,
            session_state=self.session_state,
            spinner=Mock(return_value=nullcontext()),
            error=Mock(),
        )
        self.st_patcher.start()

    def tearDown(self):
        self.st_patcher.stop()

    def test_demo_mode_loads_cache_without_calling_llm(self):
        with TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "inbox_sample.json"
            cache_path.write_text(
                '[{"from":"a@example.com","subject":"Hi","category":"FYI",'
                '"one_line_summary":"Read only.","suggested_reply":null}]',
                encoding="utf-8",
            )
            with patch.object(inbox, "CACHE_JSON", cache_path), patch.object(
                inbox.llm, "ask_claude_json"
            ) as ask_json:
                inbox._triage("ignored in demo", demo=True)

        ask_json.assert_not_called()
        self.assertEqual(self.session_state["inbox_result"]["emails"][0]["category"], "FYI")
        self.assertIn("elapsed", self.session_state["inbox_result"])

    def test_api_failure_shows_friendly_error(self):
        with patch.object(
            inbox.llm, "ask_claude_json", side_effect=inbox.llm.LLMError("Friendly failure")
        ):
            inbox._triage("From: a@example.com\nSubject: Hi", demo=False)

        inbox.st.error.assert_called_once_with("Friendly failure")
        self.assertNotIn("inbox_result", self.session_state)


if __name__ == "__main__":
    unittest.main()
