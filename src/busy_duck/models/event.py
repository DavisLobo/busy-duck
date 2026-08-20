# Event

# Business Fields
# ---------------
# id
# title
# description
# start_datetime
# end_datetime
# location
# organizer
# attendees

# Synchronization Fields
# ----------------------
# provider_id
# account_id
# external_id

# Metadata
# --------
# created_at
# updated_at
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Event(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    title: str
    start_datetime: datetime
    end_datetime: datetime

    description: Optional[str] = None
    location: Optional[str] = None

    provider_id: UUID
    account_id: UUID
    calendar_id: UUID

    external_id: str

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @model_validator(mode="after")
    def validate_datetime_order(self):
        if self.start_datetime >= self.end_datetime:
            raise ValueError("Start datetime must be before end datetime")
        return self