from app.core.security import (
    get_current_admin_user
)
from app.celery.tasks import notify_users
from app.db.models.user import User
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.product import ProductRepository
from app.db.models.user import UserRepository
from app.schemas.product import CreateProductRequest, ProductResponse, PatchProductRequest

router = APIRouter()

@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(request: CreateProductRequest, db: Session = Depends(get_db), _: User = Depends(get_current_admin_user)):
    """
    Create a product
    """
    product_repository = ProductRepository(db)
    user_repository = UserRepository(db)
    existing_product = product_repository.find_by_sku(request.sku)
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with sku '{request.sku}' already exists."
        )
    
    try:
        product = product_repository.create(request.as_dict())
        admins = user_repository.get_admins()
        email_list = [admin.username for admin in admins]
        notify_users.delay(email_list, 'create')
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

@router.get("/products/{product_sku}", response_model=ProductResponse)
def get_product(product_sku: str, db: Session = Depends(get_db)):
    """
    Get a product by sku
    """
    product_repository = ProductRepository(db)
    product = product_repository.find_by_sku(product_sku)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with sku '{product_sku}' not found."
        )
    return ProductResponse(**product.as_dict())

@router.get("/products", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    """
    List all products
    """
    product_repository = ProductRepository(db)
    products = product_repository.list()
    return [ProductResponse(**product.as_dict()) for product in products]

@router.patch("/products/{product_sku}", response_model=ProductResponse)
def update_product(
    product_sku: str,
    request: PatchProductRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user)
):
    """
    Update a product
    """
    product_repository = ProductRepository(db)
    user_repository = UserRepository(db)
    product = product_repository.find_by_sku(product_sku)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with sku '{product_sku}' not found."
        )
    
    try:
        product = product_repository.update(product, request.as_dict())
        admins = user_repository.get_admins()
        email_list = [admin.username for admin in admins]
        notify_users.delay(email_list, 'update')
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

@router.delete("/products/{product_sku}", response_model=ProductResponse)
def delete_product(product_sku: str, db: Session = Depends(get_db), _: User = Depends(get_current_admin_user)):
    """
    Delete a product
    """
    product_repository = ProductRepository(db)
    user_repository = UserRepository(db)
    product = product_repository.find_by_sku(product_sku)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with sku '{product_sku}' not found."
        )
    
    try:
        product = product_repository.delete(product)
        admins = user_repository.get_admins()
        email_list = [admin.username for admin in admins]
        notify_users.delay(email_list, 'create')
        return ProductResponse(**product.as_dict())
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error. Check your request data."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
