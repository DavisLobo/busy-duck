from __future__ import annotations

from datetime import datetime, timedelta

from busy_duck.providers.provider_registry import registry
from busy_duck.repositories.account_repository import AccountRepository
from busy_duck.repositories.calendar_repository import CalendarRepository
from busy_duck.repositories.event_repository import EventRepository
from busy_duck.repositories.provider_repository import ProviderRepository
from busy_duck.services.provider_sync_service import ProviderSyncService


class MultiProviderSyncService:
    def __init__(self, session) -> None:
        self.session = session
        self.provider_repository = ProviderRepository(session)
        self.account_repository = AccountRepository(session)
        self.calendar_repository = CalendarRepository(session)
        self.event_repository = EventRepository(session)
        self.sync_service = ProviderSyncService(self.event_repository)

    def _ensure_provider(self, provider_name: str, slug: str):
        provider = self.provider_repository.find_by_slug(slug)
        if provider is not None:
            return provider

        from busy_duck.database.models.provider_model import ProviderModel

        provider = ProviderModel(
            name=provider_name,
            slug=slug,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        return self.provider_repository.save(provider)

    def _ensure_account(self, provider_id: str, email: str, username: str):
        account = self.account_repository.find_by_email(email)
        if account is not None:
            return account

        from busy_duck.database.models.account_model import AccountModel

        account = AccountModel(
            provider_id=provider_id,
            email=email,
            username=username,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        return self.account_repository.save(account)

    def _ensure_calendar(self, account_id: str, external_id: str, name: str):
        calendar = self.calendar_repository.find_by_external_id(external_id)
        if calendar is not None:
            return calendar

        from busy_duck.database.models.calendar_model import CalendarModel

        calendar = CalendarModel(
            account_id=account_id,
            external_id=external_id,
            name=name,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        return self.calendar_repository.save(calendar)

    def sync_provider(
        self,
        provider_name: str,
        email: str,
        username: str,
        external_calendar_id: str,
        calendar_name: str,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> int:
        slug = provider_name.lower()
        provider = self._ensure_provider(provider_name, slug)
        account = self._ensure_account(provider.id, email, username)
        calendar = self._ensure_calendar(account.id, external_calendar_id, calendar_name)

        if start_datetime is None:
            start_datetime = datetime.now() - timedelta(days=7)
        if end_datetime is None:
            end_datetime = datetime.now() + timedelta(days=7)

        provider_instance = registry.create(slug)
        raw_events = provider_instance.fetch_events(start_datetime, end_datetime)

        return self.sync_service.sync_events_for_calendar(
            provider_id=provider.id,
            account_id=account.id,
            calendar_id=calendar.id,
            raw_events=raw_events,
        )

    def sync_all(
        self,
        provider_configs: list[dict],
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> dict[str, int]:
        totals: dict[str, int] = {}

        for config in provider_configs:
            totals[config["provider_name"]] = self.sync_provider(
                provider_name=config["provider_name"],
                email=config["email"],
                username=config.get("username", "User"),
                external_calendar_id=config["external_calendar_id"],
                calendar_name=config.get("calendar_name", "Principal"),
                start_datetime=start_datetime,
                end_datetime=end_datetime,
            )

        return totals