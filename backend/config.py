"""Runtime config for the FastAPI app."""
import os

from dotenv import load_dotenv

from lib import llm

APP_NAME = "OfficeFlow"
TRUE_VALUES = {"1", "true", "yes", "on"}


def demo_default() -> bool:
    load_dotenv()
    return os.getenv("DEFAULT_DEMO_MODE", "true").strip().lower() in TRUE_VALUES


def providers_available() -> list[str]:
    load_dotenv()
    keys = {
        "gemini": os.getenv("GEMINI_API_KEY"),
        "groq": os.getenv("GROQ_API_KEY"),
        "openrouter": os.getenv("OPENROUTER_API_KEY"),
    }
    return [name for name in llm.PROVIDER_ORDER if keys.get(name)]
