from datetime import datetime

from busy_duck.database.connection import get_session, initialize_database
from busy_duck.providers.google_provider import GoogleProvider
from busy_duck.providers.provider_registry import registry
from busy_duck.repositories.calendar_repository import CalendarRepository
from busy_duck.repositories.event_repository import EventRepository
from busy_duck.services.provider_sync_service import ProviderSyncService


def main() -> None:
    initialize_database()

    session = get_session()
    try:
        event_repository = EventRepository(session)
        provider_sync_service = ProviderSyncService(event_repository)

        provider = registry.create("google")
        events = provider.fetch_events(
            datetime(2025, 1, 1, 0, 0),
            datetime(2025, 1, 2, 0, 0),
        )

        # Em produção, o calendar_id e account_id vêm do banco local.
        # Aqui mostramos a integração.
        for event in events:
            event["calendar_id"] = "calendar-local-id"
            event["account_id"] = "account-local-id"

        provider_sync_service.sync_provider_events(
            provider_id="provider-google-id",
            account_id="account-local-id",
            raw_events=events,
        )
    finally:
        session.close()


if __name__ == "__main__":
    main()
