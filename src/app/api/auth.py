from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.depends_stub import Stub
from app.application.auth.auth_service import AuthService

from app.application.schemas.users import SUserIn

auth_router = APIRouter()


@auth_router.post("/register")
async def register(
    user: SUserIn,
    auth_service: Annotated[AuthService, Depends(Stub(AuthService))],
):
    user = user.to_dto()
    res = await auth_service.register_user(user)
    return res

@auth_router.post("/login")
async def login(
    user: SUserIn,
    auth_service: Annotated[AuthService, Depends(Stub(AuthService))],
):
    user = user.to_dto()
    res = await auth_service.login_user(user)
    return res

@auth_router.post("/get-token")
async def get_session(
    sessionid: str,
    auth_service: Annotated[AuthService, Depends(Stub(AuthService))],
):
    res = await auth_service.get_session(sessionid)
    return res