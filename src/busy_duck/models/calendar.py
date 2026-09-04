from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

class Calendar(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    account_id: UUID
    external_id: str
    name: str

    color: Optional[str] = None
    is_active: bool = True

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))