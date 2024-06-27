from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from app.db.models.base import BaseModel


class Plataform(BaseModel):
    __tablename__ = "plataforms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "name": self.name,
        }


class CanalRepository:
    def __init__(self, db: Session):
        self.db = db
