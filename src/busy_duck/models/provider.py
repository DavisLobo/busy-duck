from datetime import datetime, timezone

from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class Provider(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    
    name: str
    slug: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __init__(self, name: str, slug: str) -> None:
        super().__init__(name=name, slug=slug)