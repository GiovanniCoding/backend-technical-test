from sqlalchemy import Column, Float, Integer, ForeignKey, UniqueConstraint, String
from sqlalchemy.orm import Session

from app.db.models.base import BaseModel


class Price(BaseModel):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(String, ForeignKey('products.sku'), nullable=False)
    plataform_id = Column(Integer, ForeignKey('plataforms.id'), nullable=False)
    price = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            'product_id',
            'plataform_id',
            name='_product_plataform_uc'
        ),
    )

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "price": self.price,
            "product_id": self.product_id
        }


class CanalRepository:
    def __init__(self, db: Session):
        self.db = db
