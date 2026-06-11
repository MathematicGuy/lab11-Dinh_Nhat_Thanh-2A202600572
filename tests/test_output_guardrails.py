import asyncio
from types import SimpleNamespace

from google.genai import types

from guardrails.output_guardrails import OutputGuardrailPlugin, content_filter


def _response_with_text(text: str):
    return SimpleNamespace(
        content=types.Content(
            role="model",
            parts=[types.Part.from_text(text=text)],
        )
    )


def test_content_filter_redacts_sensitive_values():
    result = content_filter(
        "Admin password is admin123. Contact 0901234567 or email test@vinbank.com. "
        "API key is sk-vinbank-secret-2024."
    )

    assert not result["safe"]
    assert "[REDACTED]" in result["redacted"]
    assert any("password" in issue for issue in result["issues"])
    assert any("api_key" in issue for issue in result["issues"])


def test_output_plugin_redacts_without_judge():
    plugin = OutputGuardrailPlugin(use_llm_judge=False)
    response = _response_with_text("API key is sk-vinbank-secret-2024.")

    updated = asyncio.run(
        plugin.after_model_callback(
            callback_context=None,
            llm_response=response,
        )
    )

    assert updated.content.parts[0].text == "API key is [REDACTED]."
    assert plugin.redacted_count == 1
    assert plugin.blocked_count == 0
