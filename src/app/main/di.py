from typing import Annotated, AsyncGenerator
from typing import Iterable
from functools import partial

from fastapi import FastAPI, Depends

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.api.depends_stub import Stub
from .config import settings

from app.application.repositories.users_rep import UsersRepository
from app.application.services.users import UsersService
from app.application.auth.auth_service import AuthService

async_engine = create_async_engine(settings.dsn_asyncpg, echo=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
        
def get_service(
    service, repo, session: Annotated[AsyncSession, Depends(Stub(AsyncSession))]
):
    return service(repo(session))

def get_auth_service(
    user_service: Annotated[UsersService, Depends(Stub(UsersService))],
):
    return AuthService(user_service)

def init_dependencies(app: FastAPI) -> None:
    app.dependency_overrides[AsyncSession] = get_async_session
    app.dependency_overrides[UsersService] = partial(
        get_service, UsersService, UsersRepository
    )
    app.dependency_overrides[AuthService] = get_auth_service
    # app.dependency_overrides[UserServiceSync] = partial(
    #     get_service_sync, UserServiceSync, UserRepositorySync
    # )
