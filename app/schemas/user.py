from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    id: UUID
    username: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

class UserDeletedResponse(BaseModel):
    id: UUID
    deleted_at: datetime

class PatchUserRequest(BaseModel):
    username: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    password: Optional[str] = None

    def as_dict(self) -> dict:
        return {
            'username': self.username,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'password': self.password,
        }
