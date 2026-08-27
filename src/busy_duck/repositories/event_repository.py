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
    
    def find_by_calendar_id(self, calendar_id: str) -> list[EventModel]:
        return self.session.filter(EventModel.calendar_id == calendar_id).all()
    
    def find_by_external_id(self, external_id: str) -> EventModel | None:
        return self.session.query(EventModel).filter(EventModel.external_id == external_id).first()
    
    def delete(self, event: EventModel) -> None:
        self.session.delete(event)
        self.session.commit()