"""Shared Streamlit Cloud defaults for OfficeFlow."""
import streamlit as st


TRUE_VALUES = {"1", "true", "yes", "on"}


def get_secret(name: str, default=None):
    """Read a Streamlit secret without failing outside Streamlit Cloud."""
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


def _truthy(value) -> bool:
    return str(value).strip().lower() in TRUE_VALUES


def default_demo_mode() -> bool:
    """Public deployments default to cached demo output unless explicitly disabled."""
    return _truthy(get_secret("DEFAULT_DEMO_MODE", "true"))


def live_minutes_enabled() -> bool:
    """Allow Whisper only when the deployment is not configured as public demo-first."""
    override = get_secret("ENABLE_LIVE_MINUTES", None)
    if override is not None:
        return _truthy(override)
    return not default_demo_mode()
