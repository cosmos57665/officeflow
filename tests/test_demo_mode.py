import json
import unittest
from contextlib import nullcontext
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

import pandas as pd

from modules import docs, minutes


class DemoModeOfflineTests(unittest.TestCase):
    def test_minutes_demo_uses_cache_without_transcribe_or_llm(self):
        session_state = {}
        cached = {
            "title": "Demo Minutes",
            "date": "5 July 2026",
            "attendees": ["Asha"],
            "summary": ["Reviewed demo readiness."],
            "action_items": [],
            "decisions": ["Use cached fallback."],
        }
        with TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "minutes_sample.json"
            output_dir = Path(tmp) / "outputs"
            cache_path.write_text(json.dumps(cached), encoding="utf-8")
            with patch.multiple(
                minutes.st,
                session_state=session_state,
                spinner=Mock(return_value=nullcontext()),
                error=Mock(),
            ), patch.object(minutes, "CACHE_JSON", cache_path), patch.object(
                minutes, "OUTPUT_DIR", output_dir
            ), patch.object(minutes.transcribe, "transcribe") as transcribe_audio, patch.object(
                minutes.llm, "ask_claude_json"
            ) as ask_json:
                minutes._run(None, demo=True)

        transcribe_audio.assert_not_called()
        ask_json.assert_not_called()
        self.assertEqual(session_state["minutes_result"]["data"]["title"], "Demo Minutes")
        self.assertGreater(len(session_state["minutes_result"]["docx_bytes"]), 0)

    def test_docs_demo_uses_cache_without_llm(self):
        session_state = {}
        df = pd.DataFrame([
            {
                "name": "Asha Rao",
                "class": "10A",
                "marks": 91,
                "achievement": "Science fair winner",
            }
        ])
        cached = [{"name": "Asha Rao", "remark": "Asha is ready for the demo."}]
        with TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "remarks_sample.json"
            output_dir = Path(tmp) / "certificates"
            cache_path.write_text(json.dumps(cached), encoding="utf-8")
            with patch.multiple(
                docs.st,
                session_state=session_state,
                spinner=Mock(return_value=nullcontext()),
                error=Mock(),
            ), patch.object(docs, "CACHE_JSON", cache_path), patch.object(
                docs, "OUTPUT_DIR", output_dir
            ), patch.object(docs.llm, "ask_claude_json") as ask_json:
                docs._run(df, "Merit Certificate", demo=True)

        ask_json.assert_not_called()
        self.assertEqual(session_state["docs_result"]["count"], 1)
        self.assertGreater(len(session_state["docs_result"]["zip"]), 0)


if __name__ == "__main__":
    unittest.main()
