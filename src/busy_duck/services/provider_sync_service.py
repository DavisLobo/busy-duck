from __future__ import annotations

from datetime import datetime
from typing import Any

from busy_duck.database.models.event_model import EventModel
from busy_duck.repositories.event_repository import EventRepository


class ProviderSyncService:
    def __init__(self, event_repository: EventRepository) -> None:
        self.event_repository = event_repository

    def _normalize_event(
        self,
        provider_id: str,
        account_id: str,
        raw_event: dict[str, Any],
    ) -> EventModel:
        return EventModel(
            calendar_id=raw_event["calendar_id"],
            provider_id=provider_id,
            account_id=account_id,
            external_id=str(raw_event["external_id"]),
            title=str(raw_event["title"]),
            description=raw_event.get("description"),
            location=raw_event.get("location"),
            start_datetime=raw_event["start_datetime"],
            end_datetime=raw_event["end_datetime"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def sync_provider_events(
        self,
        provider_id: str,
        account_id: str,
        raw_events: list[dict[str, Any]],
    ) -> int:
        synchronized = 0

        for raw_event in raw_events:
            event = self._normalize_event(provider_id, account_id, raw_event)

            existing = self.event_repository.find_by_provider_and_external_id(
                provider_id,
                event.external_id,
            )

            if existing is None:
                self.event_repository.save(event)
            else:
                existing.calendar_id = event.calendar_id
                existing.account_id = event.account_id
                existing.title = event.title
                existing.description = event.description
                existing.location = event.location
                existing.start_datetime = event.start_datetime
                existing.end_datetime = event.end_datetime
                existing.updated_at = event.updated_at
                self.event_repository.save(existing)

            synchronized += 1

        return synchronized

    def sync_events_for_calendar(
        self,
        provider_id: str,
        account_id: str,
        calendar_id: str,
        raw_events: list[dict[str, Any]],
    ) -> int:
        normalized: list[dict[str, Any]] = []
        for raw_event in raw_events:
            event_data = dict(raw_event)
            event_data["calendar_id"] = calendar_id
            normalized.append(event_data)

        return self.sync_provider_events(provider_id, account_id, normalized)