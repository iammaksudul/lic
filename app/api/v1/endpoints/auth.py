from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import create_access_token
from app.db.session import get_db
from app.services import auth as auth_service
from pydantic import BaseModel

# Define response model for login
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    role: str

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> LoginResponse:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    # Authenticate the user using the email and password
    user = auth_service.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    
    # If user is not found or credentials are incorrect
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # If the user is inactive
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create an access token with an expiration time
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user.id, expires_delta=access_token_expires
    )
    
    # Return the token and user information
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        role=user.role
    )
