from __future__ import annotations

from datetime import datetime
from typing import Any

from busy_duck.config import settings
from busy_duck.providers.base_provider import BaseProvider


class GoogleProvider(BaseProvider):
    provider_name = "google"

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(config)
        self.client: Any | None = None

    def connect(self) -> None:
        # Replace this with real Google OAuth client creation.
        self.client = {
            "connected": True,
            "provider": self.name,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        }

    def fetch_events(
        self,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> list[dict[str, Any]]:
        self.connect()

        day = start_datetime.replace(
            hour=9,
            minute=0,
            second=0,
            microsecond=0,
        )

        return [
            {
                "external_id": "google-event-1",
                "calendar_id": "calendar-google-primary",
                "title": "Daily sync",
                "description": "Daily sync with team",
                "location": "Remote",
                "start_datetime": day,
                "end_datetime": day.replace(hour=10),
            },
            {
                "external_id": "google-event-2",
                "calendar_id": "calendar-google-primary",
                "title": "Planning",
                "description": "Sprint planning",
                "location": "Office",
                "start_datetime": day.replace(hour=9, minute=30),
                "end_datetime": day.replace(hour=10, minute=30),
            },
        ]