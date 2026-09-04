from __future__ import annotations

from datetime import datetime, timedelta

from busy_duck.config import settings
from busy_duck.database.connection import get_session, initialize_database
from busy_duck.services.analytics_service import AnalyticsService
from busy_duck.services.calendar_service import CalendarService
from busy_duck.repositories.calendar_repository import CalendarRepository
from busy_duck.repositories.event_repository import EventRepository
from busy_duck.services.multi_provider_sync_service import MultiProviderSyncService


def bootstrap_app() -> None:
    initialize_database()


def sync_all(
    provider_configs: list[dict] | None = None,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
) -> dict[str, int]:
    if provider_configs is None:
        provider_configs = [
            {
                "provider_name": "google",
                "email": "user@gmail.com",
                "username": "Test User",
                "external_calendar_id": "calendar-google-primary",
                "calendar_name": "Principal",
            },
            {
                "provider_name": "outlook",
                "email": "user@outlook.com",
                "username": "Test User",
                "external_calendar_id": "calendar-outlook-primary",
                "calendar_name": "Principal",
            },
        ]

    if start_datetime is None:
        start_datetime = datetime.now() - timedelta(days=settings.DEFAULT_TIME_WINDOW_DAYS)
    if end_datetime is None:
        end_datetime = datetime.now() + timedelta(days=settings.DEFAULT_TIME_WINDOW_DAYS)

    session = get_session()
    try:
        sync_service = MultiProviderSyncService(session)
        return sync_service.sync_all(
            provider_configs=provider_configs,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )
    finally:
        session.close()


def get_events_in_window(
    start_datetime: datetime,
    end_datetime: datetime,
) -> list:
    session = get_session()
    try:
        event_repository = EventRepository(session)
        calendar_repository = CalendarRepository(session)
        calendar_service = CalendarService(calendar_repository, event_repository)
        return calendar_service.list_events(start_datetime, end_datetime)
    finally:
        session.close()


def get_analytics_for_window(
    start_datetime: datetime,
    end_datetime: datetime,
) -> dict:
    events = get_events_in_window(start_datetime, end_datetime)
    analytics = AnalyticsService()
    conflicts = analytics.find_conflicts(events)
    free_time = analytics.calculate_free_time(events, start_datetime, end_datetime)

    return {
        "events_count": len(events),
        "conflicts_count": len(conflicts),
        "free_time": free_time,
    }


def main() -> None:
    bootstrap_app()


if __name__ == "__main__":
    main()
