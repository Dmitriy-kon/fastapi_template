from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import HTTPBasicCredentials

from app.api.depends_stub import Stub
from app.application.auth.auth_service import AuthService

from app.application.schemas.users import SUserIn
from app.application.dto.users import UserDTO

from app.application.auth.auth_session import security

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
    request: Request,
    response: Response,
):
    user = user.to_dto()
    res = await auth_service.login_user(user, request)
    
    # return res
    response.set_cookie("session_id", res)
    return {"message": "all good"}

@auth_router.post("/login-basic")
async def login_httpbasic(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    auth_service: Annotated[AuthService, Depends(Stub(AuthService))],
    request: Request,
    response: Response
    
):
    user = UserDTO(name=credentials.username, hashed_password=credentials.password)
    res = await auth_service.login_user(user, request)
    
    response.set_cookie("session_id", res)
    return {"message": "all good", "headers": response.headers}
