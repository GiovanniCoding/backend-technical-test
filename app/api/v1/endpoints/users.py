from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_admin_user, get_current_user
from app.db.database import get_db
from app.db.models.user import User, UserRepository
from app.schemas.user import PatchUserRequest, UserDeletedResponse, UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_me(user: User = Depends(get_current_user)):
    """
    Get the current user
    """
    return user


@router.get("/users/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_users(
    id: UUID, db: Session = Depends(get_db), _: User = Depends(get_current_admin_user)
):
    """
    Get a users (admin only)
    """
    user_repositoy = UserRepository(db)
    return user_repositoy.get_by_id(id)


@router.get("/users", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db), _: User = Depends(get_current_admin_user)):
    """
    Get all users (admin only)
    """
    user_repositoy = UserRepository(db)
    users = user_repositoy.list()
    return [UserResponse(**user.as_dict()) for user in users]


@router.patch(
    "/users/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
def update_user(
    id: UUID,
    request: PatchUserRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    """
    Update a user (admin only)
    """
    try:
        existing_user = UserRepository(db).get_by_email(request.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email '{request.email}' already exists.",
            )
        existing_user = UserRepository(db).get_by_username(request.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with username '{request.username}' already exists.",
            )
        user_repositoy = UserRepository(db)
        user = user_repositoy.update(id, request.as_dict())
        return UserResponse(**user.as_dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete(
    "/users/{id}",
    response_model=UserDeletedResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def delete_user(
    id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    """
    Delete a user (admin only)
    """
    user_repositoy = UserRepository(db)
    existing_user = user_repositoy.get_by_id(id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{id}' not found.",
        )
    response = user_repositoy.delete(id)
    return UserDeletedResponse(
        id=response.id,
        deleted_at=response.deleted_at,
    )
