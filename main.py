from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models import models
from auth.auth import auth_backend
from auth.db import User, get_async_session
from auth.manager import get_user_manager
from models.schemas import UserRead, UserCreate, BlogCreate


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app = FastAPI(
    title="Blog app"
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


current_user = fastapi_users.current_user()


@app.get("/blogs")
async def get_blogs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_session)):
    """Async function for get all blogs from db"""
    try:
        blogs = await db.execute(select(models.Blog).offset(skip).limit(limit))
        result = blogs.scalars().all()
        return result

    except SQLAlchemyError as e:
        """DB error"""
        return {"error": str(e)}


@app.get("/blog/{blog_id}")
async def get_blog_by_id(blog_id: int, db: AsyncSession = Depends(get_async_session)):
    """Async function for get blog by id from db"""
    try:
        blog = await db.execute(select(models.Blog).filter(models.Blog.id == blog_id))
        result = blog.scalars().first()
        return result

    except SQLAlchemyError as e:
        """DB error"""
        return {"error": str(e)}


@app.post("/blog/create/")
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
