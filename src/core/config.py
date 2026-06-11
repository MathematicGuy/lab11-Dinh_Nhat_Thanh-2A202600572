"""
Lab 11 — Configuration & API Key Setup
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

GOOGLE_MODEL_NAME = "gemini-2.5-flash-lite"
# The installed LiteLLM catalog exposes OpenRouter DeepSeek V4 Flash.
OPENROUTER_LITELLM_MODEL = "openrouter/deepseek/deepseek-v4-flash"
OPENROUTER_CHAT_MODEL = "deepseek/deepseek-v4-flash"


def get_model_provider() -> str | None:
    """Return the first available live model provider."""
    if os.environ.get("OPENAI_API_KEY", "").strip():
        return "openai"
    if os.environ.get("GOOGLE_API_KEY", "").strip():
        return "google"
    if os.environ.get("OPENROUTER_API_KEY", "").strip():
        return "openrouter"
    return None


def get_adk_model():
    """Return an ADK-compatible model spec for the active provider."""
    provider = get_model_provider()
    if provider == "openai":
        from google.adk.models import LiteLlm
        model_name = os.environ.get("MODEL_ID", "gpt-5.4-nano").strip()
        # Fall back to gpt-4o-mini if nano is not available
        return LiteLlm(
            model=f"openai/{model_name}",
            fallbacks=["openai/gpt-4o-mini"]
        )
    if provider == "google":
        return GOOGLE_MODEL_NAME
    if provider == "openrouter":
        from google.adk.models import LiteLlm

        return LiteLlm(model=OPENROUTER_LITELLM_MODEL)
    raise RuntimeError(
        "No live model provider configured. Set OPENAI_API_KEY, GOOGLE_API_KEY, or OPENROUTER_API_KEY."
    )


def setup_api_key():
    """Load API key from environment or prompt when interactive.

    Returns:
        True when a key is available, False otherwise.
    """
    if get_model_provider() is None:
        if sys.stdin is not None and sys.stdin.isatty():
            try:
                os.environ["GOOGLE_API_KEY"] = input("Enter Google API Key: ")
            except EOFError:
                print(
                    "No OPENAI_API_KEY, GOOGLE_API_KEY, or OPENROUTER_API_KEY available. "
                    "Skipping live model calls."
                )
                return False
        else:
            print(
                "No OPENAI_API_KEY, GOOGLE_API_KEY, or OPENROUTER_API_KEY set. "
                "Skipping live model calls."
            )
            return False
    
    provider = get_model_provider()
    if provider == "openai":
        model_name = os.environ.get("MODEL_ID", "gpt-5.4-nano").strip()
        print(f"API key loaded. Provider: OpenAI (preferred: {model_name}, fallback: gpt-4o-mini)")
    elif provider == "google":
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "0"
        print("API key loaded. Provider: Google")
    elif provider == "openrouter":
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
