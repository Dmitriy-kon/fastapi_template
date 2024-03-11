from fastapi import APIRouter

from .index import index_router
from .users import users_router
from .auth import auth_router


root_router = APIRouter()
root_router.include_router(
    index_router
)
root_router.include_router(
    users_router,
    prefix="/users",
    tags=["users"],
)
root_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"],
)