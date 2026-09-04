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
        if start_datetime >= end_datetime:
            raise ValueError("Start datetime must be before end datetime")

        intervals = sorted(
            (
                max(event.start_datetime, start_datetime),
                min(event.end_datetime, end_datetime),
            )
            for event in events
            if event.start_datetime < end_datetime
            and event.end_datetime > start_datetime
        )

        busy_duration = timedelta()

        for interval_start, interval_end in intervals:
            if interval_start >= interval_end:
                continue

            if not busy_duration:
                current_start = interval_start
                current_end = interval_end
                busy_duration = current_end - current_start
                continue

            if interval_start <= current_end:
                if interval_end > current_end:
                    busy_duration += interval_end - current_end
                    current_end = interval_end
            else:
                busy_duration += interval_end - interval_start
                current_start = interval_start
                current_end = interval_end

        return max(
            (end_datetime - start_datetime) - busy_duration,
            timedelta(),
        )
