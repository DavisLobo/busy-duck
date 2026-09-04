from __future__ import annotations

from datetime import datetime
from typing import Any

from busy_duck.config import settings
from busy_duck.providers.base_provider import BaseProvider


class OutlookProvider(BaseProvider):
    provider_name = "outlook"

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(config)
        self.client: Any | None = None

    def connect(self) -> None:
        # Replace this with real Microsoft Graph OAuth client creation.
        self.client = {
            "connected": True,
            "provider": self.name,
            "client_id": settings.OUTLOOK_CLIENT_ID,
            "redirect_uri": settings.OUTLOOK_REDIRECT_URI,
        }

    def fetch_events(
        self,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> list[dict[str, Any]]:
        self.connect()

        day = start_datetime.replace(
            hour=11,
            minute=0,
            second=0,
            microsecond=0,
        )

        return [
            {
                "external_id": "outlook-event-1",
                "calendar_id": "calendar-outlook-primary",
                "title": "Client sync",
                "description": "Sync with client",
                "location": "Teams",
                "start_datetime": day,
                "end_datetime": day.replace(hour=12),
            },
            {
                "external_id": "outlook-event-2",
                "calendar_id": "calendar-outlook-primary",
                "title": "Ops review",
                "description": "Operations review",
                "location": "Remote",
                "start_datetime": day.replace(hour=13, minute=30),
                "end_datetime": day.replace(hour=14, minute=30),
            },
        ]