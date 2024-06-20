from datetime import UTC, datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import Column, Float, String, Integer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models.base import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    sku = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    brand = Column(String, nullable=False)
    visit_count = Column(Integer, default=0)

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "sku": self.sku,
            "name": self.name,
            "price": self.price,
            "brand": self.brand,
            "visit_count": self.visit_count,
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
        product = self.db.query(Product).filter(
            Product.sku == sku,
            Product.deleted_at == None,
        ).first()
        if product:
            product.visit_count += 1
            self.db.commit()
            self.db.refresh(product)
        return product

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
        products = self.db.query(Product).filter(
            Product.deleted_at == None,
        ).all()
        for product in products:
            product.visit_count += 1
        self.db.commit()
        return products
