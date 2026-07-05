import os
import unittest
from unittest.mock import patch

from lib import llm


class LLMFailureMessageTests(unittest.TestCase):
    def test_api_key_prefers_streamlit_secrets_over_env(self):
        old_client = llm._client
        llm._client = None
        try:
            with patch.object(llm, "st", create=True) as fake_st, patch.dict(
                os.environ, {"ANTHROPIC_API_KEY": "env-key"}, clear=True
            ), patch.object(llm, "Anthropic", return_value="client") as anthropic:
                fake_st.secrets = {"ANTHROPIC_API_KEY": "secret-key"}

                self.assertEqual(llm._get_client(), "client")
        finally:
            llm._client = old_client

        anthropic.assert_called_once_with(api_key="secret-key")

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
