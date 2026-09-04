from datetime import datetime

from busy_duck.database.models.event_model import EventModel
from busy_duck.repositories.calendar_repository import CalendarRepository
from busy_duck.repositories.event_repository import EventRepository


class CalendarService:
    def __init__(
        self,
        calendar_repository: CalendarRepository,
        event_repository: EventRepository,
    ) -> None:
        self.calendar_repository = calendar_repository
        self.event_repository = event_repository

    def list_active_calendars(self):
        return self.calendar_repository.find_active()

    def list_events(
        self,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> list[EventModel]:
        return self.event_repository.find_between(
            start_datetime,
            end_datetime,
        )

    def list_calendar_events(self, calendar_id: str) -> list[EventModel]:
        return self.event_repository.find_by_calendar_id(calendar_id)
