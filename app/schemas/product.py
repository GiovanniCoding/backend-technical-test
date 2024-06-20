from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class CreateProductRequest(BaseModel):
    sku: str = Field(..., description="Stock Keeping Unit, must be unique")
    name: str = Field(..., description="Name of the product")
    price: float = Field(
        ..., gt=0, description="Price of the product as a positive float"
    )
    brand: str = Field(..., description="Brand of the product")

    def as_dict(self) -> dict:
        return {
            "sku": self.sku,
            "name": self.name,
            "price": self.price,
            "brand": self.brand,
        }

    @field_validator("name")
    def validate_name(cls, v):
        if not v or not (1 <= len(v) <= 100):
            raise ValueError("Name must be between 1 and 100 characters")
        return v


class ProductResponse(BaseModel):
    id: UUID
    sku: str
    name: str
    price: float
    brand: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None


class PatchProductRequest(BaseModel):
    sku: Optional[str] = None
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

    def as_dict(self) -> dict:
        return {
            "sku": self.sku,
            "name": self.name,
            "price": self.price,
            "brand": self.brand,
        }

    @field_validator("name")
    def validate_name(cls, v):
        if not v or not (1 <= len(v) <= 100):
            raise ValueError("Name must be between 1 and 100 characters")
        return v


class UserDeletedResponse(BaseModel):
    id: UUID
    deleted_at: datetime
