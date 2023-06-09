from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import get_current_user
from models import models

from auth.db import get_async_session
from models.models import User

from schemas.blog_schemas import BlogCreate, BlogUpdate


router = APIRouter(
    tags=["blog"]
)


@router.get("/blogs")
async def get_blogs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_session)):
    """Async function for get all blogs from db"""
    try:
        blogs = await db.execute(select(models.Blog).offset(skip).limit(limit))
        result = blogs.scalars().all()

        if result is None:
            return "Blogs does not exist"

        return result

    except SQLAlchemyError:
        """Database query error"""
        raise HTTPException(status_code=500, detail="Database error")


@router.get("/blog/{blog_id}")
async def get_blog_by_id(blog_id: int, db: AsyncSession = Depends(get_async_session)):
    """Async function for get blog by id from db"""
    try:
        blog = await db.execute(select(models.Blog).filter(models.Blog.id == blog_id))
        result = blog.scalars().first()

        if result is None:
            return "Blog by this id does not exist"

        return result

    except SQLAlchemyError:
        """Database query error"""
        raise HTTPException(status_code=500, detail="Database error")


@router.post("/blog/create/")
async def create_blog(blog: BlogCreate, user: Annotated[User, Depends(get_current_user)],
                      db: AsyncSession = Depends(get_async_session)):
    """Async function for create blog"""
    try:
        db_blog = models.Blog(**blog.dict(), author_id=user.id)
        db.add(db_blog)
        await db.commit()
        await db.refresh(db_blog)
        return db_blog

    except SQLAlchemyError:
        """Database query error"""
        raise HTTPException(status_code=500, detail="Database error")

    except ValidationError as e:
        """Validation error"""
        raise HTTPException(status_code=400, detail="Validation error")


@router.put("/blog/update/{blog_id}")
async def update_blog_by_id(data: BlogUpdate, blog_id: int, user: Annotated[User, Depends(get_current_user)],
                            db: AsyncSession = Depends(get_async_session)):
    """Async function for update blog by id"""
    try:
        blog = await db.execute(select(models.Blog).filter(models.Blog.id == blog_id))
        result = blog.scalars().first()

        if result is None:
            return "Blog by this id does not exist"

        if result.author_id == user.id:
            result.text = data.text
            result.name = data.name
            result.updated_at = data.updated_at
        else:
            return "You not author this blog!"

        await db.commit()
        await db.refresh(result)
        return result

    except SQLAlchemyError:
        """Database query error"""
        raise HTTPException(status_code=500, detail="Database error")


@router.get("/my/blogs")
async def get_user_blogs(user: Annotated[User, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
    """Async function for get all user blogs"""
    try:
        blogs = await db.execute(select(models.Blog).filter(models.Blog.author_id == user.id))
        result = blogs.scalars().all()

        if result is None:
            return "You do not have blogs"

        return result

    except SQLAlchemyError:
        """Database query error"""
        raise HTTPException(status_code=500, detail="Database error")

