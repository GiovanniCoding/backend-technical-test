from datetime import datetime, UTC
from uuid import UUID
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import Session

from app.db.models.base import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    sku = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    brand = Column(String, nullable=False)

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "sku": self.sku,
            "name": self.name,
            "price": self.price,
            "brand": self.brand,
        }


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db
