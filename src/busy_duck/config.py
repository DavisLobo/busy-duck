from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=False)


class Settings:
    APP_ENV = os.getenv("APP_ENV", "development")
    APP_NAME = os.getenv("APP_NAME", "busy_duck")
    DB_PATH = os.getenv("DB_PATH", str(PROJECT_ROOT / "data" / "busy_duck.db"))

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/oauth/google/callback")

    OUTLOOK_CLIENT_ID = os.getenv("OUTLOOK_CLIENT_ID", "")
    OUTLOOK_CLIENT_SECRET = os.getenv("OUTLOOK_CLIENT_SECRET", "")
    OUTLOOK_REDIRECT_URI = os.getenv("OUTLOOK_REDIRECT_URI", "http://localhost:8000/oauth/outlook/callback")

    DEFAULT_TIME_WINDOW_DAYS = int(os.getenv("DEFAULT_TIME_WINDOW_DAYS", "7"))


settings = Settings()