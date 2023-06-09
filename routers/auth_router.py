from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.auth import authenticate_user, create_access_token, get_current_user, get_password_hash
from auth.db import get_async_session
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from schemas.auth_schemas import Token, User, UserRegistrationRequest, UserRegistrationResponse
from models import models


router = APIRouter(
    tags=["auth"]
)


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_async_session)
):
    """Async function for get token after login"""
    user = await authenticate_user(db, form_data.password, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_user)]
):
    """Async function for get info about current user"""
    return current_user


@router.post("/auth/register", response_model=UserRegistrationResponse)
async def register_user(user: UserRegistrationRequest, db: AsyncSession = Depends(get_async_session)):
    """Async function for register new user"""
    try:
        if not user.username:
            raise HTTPException(status_code=422, detail="Missing username")
        if not user.email:
            raise HTTPException(status_code=422, detail="Missing email")
        new_user = models.User(username=user.username, hashed_password=get_password_hash(user.password), email=user.email)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return {"username": new_user.username, "email": new_user.email}

    except SQLAlchemyError:
        """Database query error"""
        raise HTTPException(status_code=500, detail="Database error")

    except ValidationError as e:
        """Validation error"""
        raise HTTPException(status_code=400, detail="Validation error")
