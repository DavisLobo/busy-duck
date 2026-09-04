from sqlalchemy.orm import Session

from busy_duck.database.models.calendar_model import CalendarModel


class CalendarRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, calendar: CalendarModel) -> CalendarModel:
        self.session.add(calendar)
        self.session.commit()
        self.session.refresh(calendar)

        return calendar

    def find_by_id(self, calendar_id: str) -> CalendarModel | None:
        return self.session.query(CalendarModel).filter(CalendarModel.id == calendar_id).first()

    def find_all(self) -> list[CalendarModel]:
        return self.session.query(CalendarModel).all()

    def find_by_account_id(self, account_id: str) -> list[CalendarModel]:
        return (
            self.session.query(CalendarModel)
            .filter(CalendarModel.account_id == account_id)
            .all()
        )

    def find_by_external_id(self, external_id: str) -> CalendarModel | None:
        return self.session.query(CalendarModel).filter(CalendarModel.external_id == external_id).first()

    def find_active(self) -> list[CalendarModel]:
        return (
            self.session.query(CalendarModel)
            .filter(CalendarModel.is_active.is_(True))
            .all()
        )

    def delete(self, calendar: CalendarModel) -> None:
        self.session.delete(calendar)
        self.session.commit()