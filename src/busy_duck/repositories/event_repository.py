from datetime import datetime

from sqlalchemy.orm import Session

from busy_duck.database.models.event_model import EventModel


class EventRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, event: EventModel) -> EventModel:
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event

    def find_by_id(self, event_id: str) -> EventModel | None:
        return self.session.query(EventModel).filter(EventModel.id == event_id).first()

    def find_all(self) -> list[EventModel]:
        return self.session.query(EventModel).all()

    def find_between(
        self,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> list[EventModel]:
        return (
            self.session.query(EventModel)
            .filter(
                EventModel.start_datetime < end_datetime,
                EventModel.end_datetime > start_datetime,
            )
            .order_by(EventModel.start_datetime)
            .all()
        )

    def find_by_provider_id(
        self,
        provider_id: str,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> list[EventModel]:
        query = self.session.query(EventModel).filter(EventModel.provider_id == provider_id)

        if start_datetime is not None:
            query = query.filter(EventModel.start_datetime >= start_datetime)

        if end_datetime is not None:
            query = query.filter(EventModel.end_datetime <= end_datetime)

        return query.order_by(EventModel.start_datetime).all()

    def find_by_calendar_id(self, calendar_id: str) -> list[EventModel]:
        return (
            self.session.query(EventModel)
            .filter(EventModel.calendar_id == calendar_id)
            .order_by(EventModel.start_datetime)
            .all()
        )

    def find_by_external_id(self, external_id: str) -> EventModel | None:
        return self.session.query(EventModel).filter(EventModel.external_id == external_id).first()

    def find_by_provider_and_external_id(
        self,
        provider_id: str,
        external_id: str,
    ) -> EventModel | None:
        return (
            self.session.query(EventModel)
            .filter(
                EventModel.provider_id == provider_id,
                EventModel.external_id == external_id,
            )
            .first()
        )

    def delete(self, event: EventModel) -> None:
        self.session.delete(event)
        self.session.commit()