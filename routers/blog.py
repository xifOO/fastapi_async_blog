from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import auth_backend
from auth.manager import get_user_manager
from models import models

from auth.db import User, get_async_session
from models.schemas import BlogCreate, BlogUpdate


router = APIRouter()


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


@router.get("/blogs")
async def get_blogs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_session)):
    """Async function for get all blogs from db"""
    try:
        blogs = await db.execute(select(models.Blog).offset(skip).limit(limit))
        result = blogs.scalars().all()
        return result

    except SQLAlchemyError as e:
        """DB error"""
        return {"error": str(e)}


@router.get("/blog/{blog_id}")
async def get_blog_by_id(blog_id: int, db: AsyncSession = Depends(get_async_session)):
    """Async function for get blog by id from db"""
    try:
        blog = await db.execute(select(models.Blog).filter(models.Blog.id == blog_id))
        result = blog.scalars().first()
        return result

    except SQLAlchemyError as e:
        """DB error"""
        return {"error": str(e)}


@router.post("/blog/create/")
async def create_blog(blog: BlogCreate, user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    """Async function for create blog"""
    try:
        db_blog = models.Blog(**blog.dict(), author_id=user.id)
        db.add(db_blog)
        await db.commit()
        await db.refresh(db_blog)
        return db_blog

    except SQLAlchemyError as e:
        """DB error"""
        return {"error": str(e)}

    except ValueError as e:
        """Validation Error"""
        return {"error": str(e)}


@router.put("/blog/update/{blog_id}")
async def update_blog_by_id(data: BlogUpdate, blog_id: int, user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    """Async function for update blog by id"""
    try:
        blog = await db.execute(select(models.Blog).filter(models.Blog.id == blog_id))
        result = blog.scalars().first()
        if result.author_id == user.id:
            result.text = data.text
            result.name = data.name
            result.updated_at = data.updated_at
        else:
            return "You not author this blog!"
        await db.commit()
        await db.refresh(result)
        return result
    except SQLAlchemyError as e:
        return {"error": e}