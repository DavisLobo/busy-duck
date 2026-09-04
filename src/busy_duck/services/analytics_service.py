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

        total_window = end_datetime - start_datetime

        busy_intervals = [
            (
                max(event.start_datetime, start_datetime),
                min(event.end_datetime, end_datetime),
            )
            for event in events
            if event.start_datetime < end_datetime and event.end_datetime > start_datetime
        ]

        if not busy_intervals:
            return total_window

        busy_intervals.sort(key=lambda interval: interval[0])

        merged = [list(busy_intervals[0])]

        for interval_start, interval_end in busy_intervals[1:]:
            last_start, last_end = merged[-1]
            if interval_start <= last_end:
                merged[-1][1] = max(last_end, interval_end)
            else:
                merged.append([interval_start, interval_end])

        busy_duration = timedelta()
        for interval_start, interval_end in merged:
            busy_duration += interval_end - interval_start

        return max(total_window - busy_duration, timedelta())
