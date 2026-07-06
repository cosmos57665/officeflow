from unittest.mock import patch

import pytest

from lib import llm


def test_json_fallback_uses_next_provider_after_invalid_json():
    calls = []

    def fake_call(provider, *_args, **_kwargs):
        calls.append(provider)
        if provider == "gemini":
            return "not json"
        return '{"ok": true}'

    with patch.object(llm, "_provider_enabled", return_value=True), \
            patch.object(llm, "_call_provider", side_effect=fake_call):
        data, provider = llm.ask_claude_json_with_provider("system", "user")

    assert data == {"ok": True}
    assert provider == "groq"
    assert calls == ["gemini", "groq"]


def test_text_fallback_uses_openrouter_after_two_failures():
    def fake_call(provider, *_args, **_kwargs):
        if provider in {"gemini", "groq"}:
            raise RuntimeError("down")
        return "answer"

    with patch.object(llm, "_provider_enabled", return_value=True), \
            patch.object(llm, "_call_provider", side_effect=fake_call):
        text, provider = llm.ask_claude_with_provider("system", "user")

    assert text == "answer"
    assert provider == "openrouter"


def test_all_providers_fail_with_demo_hint():
    with patch.object(llm, "_provider_enabled", return_value=True), \
            patch.object(llm, "_call_provider", side_effect=RuntimeError("down")):
        with pytest.raises(llm.LLMError) as raised:
            llm.ask_claude("system", "user")

    assert "All AI providers failed" in str(raised.value)
    assert "Demo Mode" in str(raised.value)
