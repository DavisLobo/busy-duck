from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from busy_duck.database.models.base import Base
from busy_duck.database.models.calendar_model import CalendarModel
from busy_duck.database.models.event_model import EventModel
from busy_duck.database.models.provider_model import ProviderModel
from busy_duck.repositories.calendar_repository import CalendarRepository
from busy_duck.repositories.event_repository import EventRepository


def create_session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def create_calendar(session: Session) -> CalendarModel:
    now = datetime(2025, 1, 1, 9)

    provider = ProviderModel(
        name="Test Provider",
        slug="test-provider",
        created_at=now,
        updated_at=now,
    )
    session.add(provider)
    session.flush()

    from busy_duck.database.models.account_model import AccountModel

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
    session.commit()
    session.refresh(calendar)

    return calendar


def create_event(
    calendar: CalendarModel,
    title: str,
    external_id: str,
) -> EventModel:
    start = datetime(2025, 1, 1, 9)

    return EventModel(
        calendar_id=calendar.id,
        provider_id=calendar.account_id,
        account_id=calendar.account_id,
        external_id=external_id,
        title=title,
        start_datetime=start,
        end_datetime=start + timedelta(hours=1),
        created_at=start,
        updated_at=start,
    )


def test_calendar_repository_finds_calendar_by_external_id():
    session = create_session()
    calendar = create_calendar(session)

    repository = CalendarRepository(session)

    result = repository.find_by_external_id("calendar-1")

    assert result is not None
    assert result.id == calendar.id

    session.close()


def test_event_repository_saves_and_queries_events_by_window():
    session = create_session()
    calendar = create_calendar(session)

    repository = EventRepository(session)
    saved = repository.save(
        create_event(calendar, "Daily meeting", "event-1")
    )

    result = repository.find_between(
        datetime(2025, 1, 1, 8),
        datetime(2025, 1, 1, 11),
    )

    assert saved.id is not None
    assert len(result) == 1
    assert result[0].title == "Daily meeting"

    session.close()


def test_event_repository_save_or_update_updates_existing_event():
    session = create_session()
    calendar = create_calendar(session)

    repository = EventRepository(session)

    original = create_event(calendar, "Original title", "event-1")
    repository.save(original)

    updated = create_event(calendar, "Updated title", "event-1")
    result = repository.save_or_update(updated)

    events = repository.find_all()

    assert result.id == original.id
    assert len(events) == 1
    assert events[0].title == "Updated title"

    session.close()