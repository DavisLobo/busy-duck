from datetime import datetime
from typing import Protocol


class WeatherConnector(Protocol):
    def get_forecast(
        self,
        location: str,
        at: datetime,
    ) -> dict[str, object]:
        ...


class WeatherService:
    def __init__(self, connector: WeatherConnector) -> None:
        self.connector = connector

    def get_event_forecast(
        self,
        location: str | None,
        at: datetime,
    ) -> dict[str, object] | None:
        if not location:
            return None

        return self.connector.get_forecast(location, at)
