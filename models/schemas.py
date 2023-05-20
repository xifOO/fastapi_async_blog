from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    """Schemas for get user"""
    username: str


class UserCreate(schemas.BaseUserCreate):
    """Schemas for create user"""
    email: EmailStr
    username: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class BlogBase(schemas.BaseModel):
    """Base schemas for blogs"""
    name: str
    text: str


class BlogCreate(BlogBase):
    """Schemas for create blog"""
    pass

