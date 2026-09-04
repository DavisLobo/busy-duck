from datetime import datetime, timedelta

import pytest

from busy_duck.database.models.event_model import EventModel
from busy_duck.providers.google_provider import GoogleProvider
from busy_duck.providers.outlook_provider import OutlookProvider
from busy_duck.services.analytics_service import AnalyticsService


def event(
    title: str,
    start: datetime,
    duration: int = 60,
) -> EventModel:
    return EventModel(
        calendar_id="calendar-1",
        provider_id="provider-1",
        account_id="account-1",
        external_id=title,
        title=title,
        start_datetime=start,
        end_datetime=start + timedelta(minutes=duration),
        created_at=start,
        updated_at=start,
    )

def test_analytics_detects_overlapping_events():
    start = datetime(2025, 1, 1, 9)

    events = [
        event("First", start, 60),
        event("Second", start + timedelta(minutes=30), 60),
        event("Third", start + timedelta(hours=2), 60),
    ]

    conflicts = AnalyticsService().find_conflicts(events)

    assert len(conflicts) == 1
    assert {item.title for item in conflicts[0]} == {"First", "Second"}


def test_analytics_merges_overlapping_intervals_when_calculating_free_time():
    start = datetime(2025, 1, 1, 9)
    end = datetime(2025, 1, 1, 17)

    events = [
        event("First", start, 120),
        event("Second", start + timedelta(hours=1), 120),
    ]

    free_time = AnalyticsService().calculate_free_time(
        events,
        start,
        end,
    )

    assert free_time == timedelta(hours=5)


def test_analytics_returns_full_window_when_no_events_exist():
    start = datetime(2025, 1, 1, 9)
    end = datetime(2025, 1, 1, 17)

    free_time = AnalyticsService().calculate_free_time(
        [],
        start,
        end,
    )

    assert free_time == timedelta(hours=8)


def test_analytics_rejects_invalid_window():
    start = datetime(2025, 1, 1, 9)

    with pytest.raises(ValueError):
        AnalyticsService().calculate_free_time([], start, start)


@pytest.mark.parametrize(
    ("provider_class", "expected_title"),
    [
        (GoogleProvider, "Daily sync"),
        (OutlookProvider, "Client sync"),
    ],
)
def test_demo_providers_return_events_inside_requested_day(
    provider_class,
    expected_title,
):
    start = datetime(2025, 1, 10, 8)
    end = datetime(2025, 1, 11, 8)

    events = provider_class().fetch_events(start, end)

    assert events
    assert expected_title in {item["title"] for item in events}

    for item in events:
        assert item["start_datetime"] < item["end_datetime"]
        assert item["external_id"]
        assert item["calendar_id"]


def test_event_stores_valid_datetime_values():
    start = datetime(2025, 1, 1, 10)

    item = event("Meeting", start, duration=60)

    assert item.start_datetime == start
    assert item.end_datetime == datetime(2025, 1, 1, 11)