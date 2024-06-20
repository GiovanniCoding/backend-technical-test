from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    is_active: bool = True
    is_admin: bool = False


class UserCreate(UserBase):
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: UUID
    username: str
    is_active: bool
    is_admin: bool

class UserDeletedResponse(UserBase):
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
