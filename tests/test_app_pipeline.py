from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from busy_duck import app
from busy_duck.database.models.account_model import AccountModel
from busy_duck.database.models.base import Base
from busy_duck.database.models.calendar_model import CalendarModel
from busy_duck.database.models.event_model import EventModel
from busy_duck.database.models.provider_model import ProviderModel
from busy_duck.repositories.calendar_repository import CalendarRepository
from busy_duck.repositories.event_repository import EventRepository
from busy_duck.services.analytics_service import AnalyticsService
from busy_duck.services.calendar_service import CalendarService
from busy_duck.services.sync_service import SyncService


def create_session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def test_bootstrap_initializes_database(monkeypatch):
    calls = []

    monkeypatch.setattr(
        app,
        "initialize_database",
        lambda: calls.append("initialized"),
    )

    app.bootstrap_app()

    assert calls == ["initialized"]


def test_event_sync_calendar_and_analytics_pipeline():
    session = create_session()

    now = datetime.utcnow()

    provider = ProviderModel(
        name="Test Provider",
        slug="test-provider",
        created_at=now,
        updated_at=now,
    )
    session.add(provider)
    session.flush()

    account = AccountModel(
        provider_id=provider.id,
        email="test@example.com",
        username="Test User",
        created_at=now,
        updated_at=now,
    )
    session.add(account)
    session.flush()

    calendar = CalendarModel(
        account_id=account.id,
        external_id="calendar-1",
        name="Work",
        created_at=now,
        updated_at=now,
    )
    session.add(calendar)
    session.flush()

    start = datetime(2025, 1, 1, 9)

    events = [
        EventModel(
            calendar_id=calendar.id,
            provider_id=provider.id,
            account_id=account.id,
            external_id="event-1",
            title="Daily meeting",
            start_datetime=start,
            end_datetime=start + timedelta(hours=1),
            created_at=start,
            updated_at=start,
        ),
        EventModel(
            calendar_id=calendar.id,
            provider_id=provider.id,
            account_id=account.id,
            external_id="event-2",
            title="Planning",
            start_datetime=start + timedelta(minutes=30),
            end_datetime=start + timedelta(hours=2),
            created_at=start,
            updated_at=start,
        ),
    ]

    event_repository = EventRepository(session)
    sync_service = SyncService(event_repository)

    assert sync_service.synchronize_events(events) == 2

    calendar_service = CalendarService(
        CalendarRepository(session),
        event_repository,
    )

    listed_events = calendar_service.list_events(
        start,
        start + timedelta(hours=3),
    )

    assert len(listed_events) == 2
    assert len(calendar_service.list_calendar_events(calendar.id)) == 2

    analytics_service = AnalyticsService()

    conflicts = analytics_service.find_conflicts(listed_events)
    assert len(conflicts) == 1

    free_time = analytics_service.calculate_free_time(
        listed_events,
        start,
        start + timedelta(hours=3),
    )
    assert free_time == timedelta(hours=1)

    session.close()
