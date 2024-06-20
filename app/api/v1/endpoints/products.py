from app.core.security import (
    get_current_admin_user
)
from app.db.models.user import User
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.product import ProductRepository
from app.schemas.product import CreateProductRequest, ProductResponse

router = APIRouter()

@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(request: CreateProductRequest, db: Session = Depends(get_db), _: User = Depends(get_current_admin_user)):
    """
    Create a product
    """
    product_repository = ProductRepository(db)
    existing_product = product_repository.find_by_sku(request.sku)
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with sku '{request.sku}' already exists."
        )
    
    try:
        product = product_repository.create(request.as_dict())
        return ProductResponse(**product.as_dict())
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error. Check your request data."
        )
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=ve.errors()
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
