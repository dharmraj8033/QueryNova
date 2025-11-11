"""Helper utilities for accessing deployment secrets."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

try:  # Optional dependency during local development
    import streamlit as st  # type: ignore
except Exception:  # pragma: no cover - Streamlit not installed
    st = None  # type: ignore

try:  # Load local .env values for developers
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - python-dotenv not installed
    load_dotenv = None  # type: ignore

if load_dotenv:  # pragma: no cover - side-effect during import
    root_dir = Path(__file__).resolve().parents[2]
    dotenv_path = root_dir / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path)


@lru_cache(maxsize=None)
def get_secret(name: str, *, default: Optional[str] = None, allow_placeholder: bool = False) -> Optional[str]:
    """Return a secret value, preferring Streamlit Cloud configuration.

    Secrets are resolved in the following order:
    1. Streamlit `st.secrets`
    2. Environment variables
    3. Optional default value

    Parameters
    ----------
    name:
        The configuration key to look up.
    default:
        Value returned when the secret is not defined.
    allow_placeholder:
        When ``True`` placeholder values such as ``"sk-your_openai_key_here"``
        are returned instead of being treated as missing.
    """

    if st is not None:
        try:
            if name in st.secrets:
                value = st.secrets[name]
                if _is_defined(value, allow_placeholder):
                    return value
        except Exception:  # pragma: no cover - defensive for Streamlit runtime
            pass

    value = os.getenv(name)
    if _is_defined(value, allow_placeholder):
        return value

    return default


def _is_defined(value: Optional[str], allow_placeholder: bool) -> bool:
    if value in (None, ""):
        return False
    if allow_placeholder:
        return True
    placeholders = {
        "your_serpapi_key_here",
        "sk-your_openai_key_here",
        "YOUR_SERPAPI_KEY",
        "YOUR_OPENAI_KEY",
    }
    return str(value).strip() not in placeholders
