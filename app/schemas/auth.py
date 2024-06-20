from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    email: str
    username: str
    password: str
    is_active: bool = True
    is_admin: bool = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    username: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
