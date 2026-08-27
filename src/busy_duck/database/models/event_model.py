from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from busy_duck.database.models.base import Base


class EventModel(Base):
    __tablename__ = "events"

    id: Mapped[str] = mapped_column(String(36),primary_key=True,default=lambda: str(uuid4()))

    calendar_id: Mapped[str] = mapped_column(ForeignKey("calendars.id"))

    provider_id: Mapped[str] = mapped_column(ForeignKey("providers.id"))

    account_id: Mapped[str] = mapped_column(ForeignKey("accounts.id"))

    external_id: Mapped[str] = mapped_column(String(255),index=True)

    title: Mapped[str] = mapped_column(String(255))

    description: Mapped[str | None] = mapped_column(Text,nullable=True)

    location: Mapped[str | None] = mapped_column(String(255),nullable=True)

    start_datetime: Mapped[datetime] = mapped_column(DateTime)

    end_datetime: Mapped[datetime] = mapped_column(DateTime)

    created_at: Mapped[datetime] = mapped_column(DateTime)

    updated_at: Mapped[datetime] = mapped_column(DateTime)