import os
import unittest
from unittest.mock import patch

from lib import llm


class LLMFailureMessageTests(unittest.TestCase):
    def test_missing_api_key_points_to_demo_mode(self):
        old_client = llm._client
        llm._client = None
        try:
            with patch.dict(os.environ, {}, clear=True):
                with self.assertRaises(llm.LLMError) as raised:
                    llm._get_client()
        finally:
            llm._client = old_client

        self.assertIn("Anthropic API key is missing", str(raised.exception))
        self.assertIn("Demo Mode", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
