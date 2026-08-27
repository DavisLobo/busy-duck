from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from busy_duck.database.models.base import Base


class AccountModel(Base):
    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(String(36),primary_key=True,default=lambda: str(uuid4()))

    provider_id: Mapped[str] = mapped_column(ForeignKey("providers.id"))

    email: Mapped[str] = mapped_column(String(255))
    display_name: Mapped[str] = mapped_column(String(255))

    is_active: Mapped[bool] = mapped_column(Boolean,default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)