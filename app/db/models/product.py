from datetime import UTC, datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import Column, Float, String
from sqlalchemy.exc import IntegrityError
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

    def create(self, data: dict) -> Product:
        product = Product(**data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def find_by_sku(self, sku: str) -> Product:
        return self.db.query(Product).filter(Product.sku == sku).first()

    def update(self, product: Product, data: dict) -> Product:
        data["updated_at"] = datetime.now(UTC)
        for key, value in data.items():
            if value is not None:
                setattr(product, key, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> Product:
        setattr(product, "deleted_at", datetime.now(UTC))
        self.db.commit()
        self.db.refresh(product)
        return product

    def list(self) -> list[Product]:
        return self.db.query(Product).all()
