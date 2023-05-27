import config
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from models import models
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from auth.db import get_async_session
from schemas.auth_schemas import UserInDB, TokenData


SECRET_KEY = config.SECRET

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    """Function for verify password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Function for hashing password"""
    return pwd_context.hash(password)


async def get_user(username: str, db: AsyncSession = Depends(get_async_session)):
    """Async function for get user by username"""
    try:
        query = select(models.User).filter(models.User.username == username)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        if user:
            return UserInDB(
                id=user.id,
                username=user.username,
                hashed_password=user.hashed_password,
                email=user.email
            )

    except SQLAlchemyError as e:
        """Database query error"""
        return {"error": str(e)}


async def authenticate_user(username: str, password: str, db: AsyncSession = Depends(get_async_session)):
    """Async function for authenticate user"""
    user = await get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Function for create access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_session)):
    """Async function for get current user by token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user
