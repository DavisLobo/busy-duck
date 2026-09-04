from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from busy_duck.database.models.base import Base


class CalendarModel(Base):
    __tablename__ = "calendars"

    id: Mapped[str] = mapped_column(String(36),primary_key=True,default=lambda: str(uuid4()))

    account_id: Mapped[str] = mapped_column(ForeignKey("accounts.id"))

    name: Mapped[str] = mapped_column(String(255))

    external_id: Mapped[str] = mapped_column(String(255),unique=True)

    color: Mapped[str | None] = mapped_column(String(50),nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean,default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)