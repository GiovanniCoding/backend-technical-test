from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    get_current_admin_user,
    get_password_hash,
    verify_password,
)
from app.db.database import get_db
from app.db.models.user import User, UserRepository
from app.schemas.auth import (
    TokenResponse,
    UserCreateRequest,
    UserResponse,
)

router = APIRouter()

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    """
    Get an access token for the user
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=access_token, token_type="bearer")

@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register_user(
    request: UserCreateRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    """
    Create a new user (admin only)
    """

    user = db.query(User).filter(User.username == request.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    user_repositoy = UserRepository(db)
    new_user = user_repositoy.create(
        username=request.username,
        hashed_password=get_password_hash(request.password),
        is_active=request.is_active,
        is_admin=request.is_admin,
    )
    return UserResponse(**new_user.as_dict())
