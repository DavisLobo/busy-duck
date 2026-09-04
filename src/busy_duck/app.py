from __future__ import annotations

from datetime import datetime, timedelta

from busy_duck.config import settings
from busy_duck.database.connection import get_session, initialize_database
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


def main() -> None:
    bootstrap_app()
    result = sync_all()
    print(result)


if __name__ == "__main__":
    main()
