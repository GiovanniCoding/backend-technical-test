from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.security import (
    get_current_admin_user,
    get_current_user,
)
from app.db.database import get_db
from app.db.models.user import User, UserRepository
from app.schemas.user import (
    UserResponse,
    PatchUserRequest,
    UserDeletedResponse,
)

router = APIRouter()


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_me(user: User = Depends(get_current_user)):
    """
    Get the current user
    """
    return user

@router.get("/users/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_users(id: UUID, db: Session = Depends(get_db), _: User = Depends(get_current_admin_user)):
    """
    Get all users (admin only)
    """
    user_repositoy = UserRepository(db)
    return user_repositoy.get_by_id(id)

@router.patch("/users/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(
    id: UUID,
    request: PatchUserRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    """
    Update a user (admin only)
    """
    user_repositoy = UserRepository(db)
    return user_repositoy.update(id, request.as_dict())

@router.delete("/users/{id}", response_model=UserDeletedResponse, status_code=status.HTTP_202_ACCEPTED)
def delete_user(
    id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    """
    Delete a user (admin only)
    """
    user_repositoy = UserRepository(db)
    response = user_repositoy.delete(id)
    return UserDeletedResponse(
        id=response.id,
        deleted_at=response.deleted_at,
    )
