from collections.abc import Iterable

from busy_duck.database.models.event_model import EventModel
from busy_duck.repositories.event_repository import EventRepository


class SyncService:
    def __init__(self, event_repository: EventRepository) -> None:
        self.event_repository = event_repository

    def synchronize_events(self, events: Iterable[EventModel]) -> int:
        synchronized = 0

        for incoming_event in events:
            existing_event = self.event_repository.find_by_external_id(
                incoming_event.external_id
            )

            if existing_event is None:
                self.event_repository.save(incoming_event)
            else:
                existing_event.title = incoming_event.title
                existing_event.description = incoming_event.description
                existing_event.location = incoming_event.location
                existing_event.start_datetime = incoming_event.start_datetime
                existing_event.end_datetime = incoming_event.end_datetime
                existing_event.updated_at = incoming_event.updated_at
                self.event_repository.save(existing_event)

            synchronized += 1

        return synchronized
