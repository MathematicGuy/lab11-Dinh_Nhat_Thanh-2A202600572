"""
Lab 11 — Configuration & API Key Setup
"""
import os
import sys

GOOGLE_MODEL_NAME = "gemini-2.5-flash-lite"
# The installed LiteLLM catalog exposes OpenRouter Gemini 2.5 Flash, not Flash Lite.
OPENROUTER_LITELLM_MODEL = "openrouter/google/gemini-2.5-flash"
OPENROUTER_CHAT_MODEL = "google/gemini-2.5-flash"


def get_model_provider() -> str | None:
    """Return the first available live model provider."""
    if os.environ.get("GOOGLE_API_KEY", "").strip():
        return "google"
    if os.environ.get("OPENROUTER_API_KEY", "").strip():
        return "openrouter"
    return None


def get_adk_model():
    """Return an ADK-compatible model spec for the active provider."""
    provider = get_model_provider()
    if provider == "google":
        return GOOGLE_MODEL_NAME
    if provider == "openrouter":
        from google.adk.models import LiteLlm

        return LiteLlm(model=OPENROUTER_LITELLM_MODEL)
    raise RuntimeError(
        "No live model provider configured. Set GOOGLE_API_KEY or OPENROUTER_API_KEY."
    )


def setup_api_key():
    """Load Google API key from environment or prompt when interactive.

    Returns:
        True when a key is available, False otherwise.
    """
    if get_model_provider() is None:
        if sys.stdin is not None and sys.stdin.isatty():
            try:
                os.environ["GOOGLE_API_KEY"] = input("Enter Google API Key: ")
            except EOFError:
                print(
                    "No GOOGLE_API_KEY or OPENROUTER_API_KEY available. "
                    "Skipping live model calls."
                )
                return False
        else:
            print(
                "No GOOGLE_API_KEY or OPENROUTER_API_KEY set. "
                "Skipping live model calls."
            )
            return False
    if os.environ.get("GOOGLE_API_KEY", "").strip():
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "0"
        print("API key loaded. Provider: Google")
    else:
        print(
            "API key loaded. Provider: OpenRouter "
            f"(fallback model route: {OPENROUTER_CHAT_MODEL})"
        )
    return True


# Allowed banking topics (used by topic_filter)
ALLOWED_TOPICS = [
    "banking", "account", "transaction", "transfer",
    "loan", "interest", "savings", "credit",
    "deposit", "withdrawal", "balance", "payment",
    "tai khoan", "giao dich", "tiet kiem", "lai suat",
    "chuyen tien", "the tin dung", "so du", "vay",
    "ngan hang", "atm",
]

# Blocked topics (immediate reject)
BLOCKED_TOPICS = [
    "hack", "exploit", "weapon", "drug", "illegal",
    "violence", "gambling", "bomb", "kill", "steal",
]
