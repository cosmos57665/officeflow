import os
import unittest
from unittest.mock import patch

from lib import llm


class LLMFailureMessageTests(unittest.TestCase):
    def test_api_key_prefers_streamlit_gemini_secret_over_env(self):
        old_client = llm._client
        llm._client = None
        try:
            with patch.object(llm, "st", create=True) as fake_st, patch.dict(
                os.environ, {"GEMINI_API_KEY": "env-key"}, clear=True
            ), patch.object(llm.genai, "Client", return_value="client") as client_cls:
                fake_st.secrets = {"GEMINI_API_KEY": "secret-key"}

                self.assertEqual(llm._get_client(), "client")
        finally:
            llm._client = old_client

        client_cls.assert_called_once_with(api_key="secret-key")

    def test_ask_claude_uses_gemini_generate_content(self):
        fake_client = unittest.mock.Mock()
        fake_response = unittest.mock.Mock(text="Generated reply")
        fake_client.models.generate_content.return_value = fake_response
        with patch.object(llm, "_get_client", return_value=fake_client), patch.object(
            llm.types, "GenerateContentConfig", return_value="config"
        ) as config_cls:
            reply = llm.ask_claude("System prompt", "User prompt", max_tokens=321)

        self.assertEqual(reply, "Generated reply")
        config_cls.assert_called_once_with(
            system_instruction="System prompt", max_output_tokens=321
        )
        fake_client.models.generate_content.assert_called_once_with(
            model=llm.MODEL,
            contents="User prompt",
            config="config",
        )

    def test_missing_api_key_points_to_demo_mode(self):
        old_client = llm._client
        llm._client = None
        try:
            with patch.dict(os.environ, {}, clear=True):
                with self.assertRaises(llm.LLMError) as raised:
                    llm._get_client()
        finally:
            llm._client = old_client

        self.assertIn("Gemini API key is missing", str(raised.exception))
        self.assertIn("Demo Mode", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
