from __future__ import annotations

from datetime import datetime
from typing import Any

from busy_duck.providers.base_provider import BaseProvider


class GoogleProvider(BaseProvider):
    provider_name = "google"

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(config)
        self.client: Any | None = None

    def connect(self) -> None:
        # Aqui entraria OAuth2 / Google API client.
        # Por enquanto, a conexão é apenas um stub.
        self.client = {"connected": True, "provider": self.name}

    def fetch_events(
        self,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> list[dict[str, Any]]:
        self.connect()

        # Exemplo de payload em formato bruto.
        # Em produção, isso viria do Google Calendar API.
        return [
            {
                "external_id": "google-event-1",
                "calendar_external_id": "primary",
                "calendar_name": "Principal",
                "title": "Daily sync",
                "description": "Reunião diária",
                "location": "Remote",
                "start_datetime": datetime(2025, 1, 1, 9, 0),
                "end_datetime": datetime(2025, 1, 1, 10, 0),
            },
            {
                "external_id": "google-event-2",
                "calendar_external_id": "primary",
                "calendar_name": "Principal",
                "title": "Planning",
                "description": "Planejamento de sprint",
                "location": "Office",
                "start_datetime": datetime(2025, 1, 1, 9, 30),
                "end_datetime": datetime(2025, 1, 1, 10, 30),
            },
        ]