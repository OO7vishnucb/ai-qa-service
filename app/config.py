"""
app/config.py
-------------
Central configuration — replaces your existing config.py entirely.
All settings come from environment variables / .env file.
"""
import os
from typing import List

from dotenv import load_dotenv

load_dotenv()


class Settings:
    # ── Existing settings (keep as-is) ────────────────────────────────────
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    database_url: str = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ai_service"
    )

    # ── NEW: API key auth ─────────────────────────────────────────────────
    # Comma-separated list of valid API keys, e.g.  API_KEYS=key1,key2
    _raw_keys: str = os.getenv("API_KEYS", "dev-secret-key")

    @property
    def api_keys(self) -> List[str]:
        return [k.strip() for k in self._raw_keys.split(",") if k.strip()]

    # ── NEW: App metadata ─────────────────────────────────────────────────
    app_name: str = "AI Q&A Service"
    app_version: str = "1.0.0"
    environment: str = os.getenv("ENVIRONMENT", "development")


settings = Settings()