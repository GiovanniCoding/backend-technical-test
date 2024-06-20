from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Session

from app.db.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    def as_dict(self) -> dict[str, str | int | float | None]:
        return super().as_dict() | {
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
        }


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        email: str,
        username: str,
        hashed_password: str,
        is_active: bool,
        is_admin: bool,
    ) -> User:
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            is_active=is_active,
            is_admin=is_admin,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: UUID) -> User:
        return (
            self.db.query(User)
            .filter(
                User.id == user_id,
                User.deleted_at == None,
            )
            .first()
        )

    def get_admins(self) -> list[User]:
        return (
            self.db.query(User)
            .filter(User.is_admin == True, User.deleted_at == None)
            .all()
        )

    def get_by_email(self, email: str) -> User:
        return (
            self.db.query(User)
            .filter(
                User.email == email,
                User.deleted_at == None,
            )
            .first()
        )

    def get_by_username(self, username: str) -> User:
        return (
            self.db.query(User)
            .filter(
                User.username == username,
                User.deleted_at == None,
            )
            .first()
        )

    def update(self, user_id: UUID, data: dict) -> User:
        data["updated_at"] = datetime.now(UTC)
        user = self.get_by_id(user_id)
        for key, value in data.items():
            if value is not None:
                setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: UUID) -> User:
        user = self.get_by_id(user_id)
        setattr(user, "deleted_at", datetime.now(UTC))
        self.db.commit()
        self.db.refresh(user)
        return user

    def list(self) -> list[User]:
        return (
            self.db.query(User)
            .filter(
                User.deleted_at == None,
                User.is_active == True,
            )
            .all()
        )
