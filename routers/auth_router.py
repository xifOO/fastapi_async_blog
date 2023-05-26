from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from auth.manager import get_user_manager
from models.models import User
from models.schemas import UserRead, UserCreate

router = APIRouter()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
