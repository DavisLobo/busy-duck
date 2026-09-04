from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class BaseProvider(ABC):
    provider_name: str = "base"

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or {}

    @property
    def name(self) -> str:
        return self.provider_name

    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def fetch_events(
        self,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> list[dict[str, Any]]:
        raise NotImplementedError