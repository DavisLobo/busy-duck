from datetime import datetime, timedelta

from busy_duck.database.models.event_model import EventModel


class AnalyticsService:
    def find_conflicts(self, events: list[EventModel]) -> list[tuple[EventModel, EventModel]]:
        ordered_events = sorted(events, key=lambda event: event.start_datetime)
        conflicts = []

        for index, event in enumerate(ordered_events):
            for next_event in ordered_events[index + 1:]:
                if next_event.start_datetime >= event.end_datetime:
                    break
                conflicts.append((event, next_event))

        return conflicts

    def calculate_free_time(
        self,
        events: list[EventModel],
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> timedelta:
        busy_duration = timedelta()
        for event in sorted(events, key=lambda item: item.start_datetime):
            start = max(event.start_datetime, start_datetime)
            end = min(event.end_datetime, end_datetime)
            if start < end:
                busy_duration += end - start

        window_duration = end_datetime - start_datetime
        return max(window_duration - busy_duration, timedelta())
