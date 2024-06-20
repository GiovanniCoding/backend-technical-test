from uuid import UUID
from pydantic import BaseModel, EmailStr

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
