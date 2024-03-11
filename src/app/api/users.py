from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.schemas.users import SUser, SUserIn
from app.api.depends_stub import Stub

from app.application.dto.users import UserDTO


from app.application.services.users import UsersService


users_router = APIRouter()


@users_router.get("/")
async def get_all_users(
    users_service: Annotated[UsersService, Depends(Stub(UsersService))],
) -> list[SUser]:
    res = await users_service.get_all_users()
    return res


@users_router.get("/{user_id}")
async def get_user_by_id(
    user_id: int,
    users_service: Annotated[UsersService, Depends(Stub(UsersService))],
) -> SUser:
    res = await users_service.get_user_by_id(user_id)
    return res

@users_router.post("/")
async def create_user(
    user: SUserIn,
    users_service: Annotated[UsersService, Depends(Stub(UsersService))],
) -> SUser:
    user = user.to_dto()
    res = await users_service.create_user(user)
    return res