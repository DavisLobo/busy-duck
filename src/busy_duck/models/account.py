from pydantic import BaseModel, Field, EmailStr
from uuid import UUID, uuid4
from datetime import datetime, timezone

class Account(BaseModel):
    """
    Account model representing user account information.
    """
    id: UUID = Field(default_factory=uuid4)
    provider_id: UUID = Field(..., description="Unique identifier for the account provider")
    
    username: str
    email: EmailStr
    is_active: bool = True
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))