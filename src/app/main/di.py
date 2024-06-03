from functools import partial
from typing import Annotated, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from fastapi import Depends, FastAPI


from app.api.depends_stub import Stub, wrap_factory
from app.application.auth.auth_service import AuthService
from app.application.repositories.users_rep import UsersRepository
from app.application.services.users import UsersService

from app.adapters.redisDb.redis_gateway import SessionRedisHandler




from .config import settings

async_engine = create_async_engine(settings.dsn_asyncpg, echo=True)


async def get_async_session(async_session) -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

def get_user_repository(session: Annotated[AsyncSession, Depends(Stub(AsyncSession))]):
    return UsersRepository(session)

def get_user_service(
    user_repo: Annotated[UsersRepository, Depends(Stub(UsersRepository))],
):
    return UsersService(user_repo)


def get_auth_service(
    user_service: Annotated[UsersService, Depends(Stub(UsersService))],
    session_handler: Annotated[SessionRedisHandler, Depends(Stub(SessionRedisHandler))],
):
    return AuthService(user_service, session_handler)

def get_session_redis_handler():
    return SessionRedisHandler()

# def get_hasher():
#     return Hasher()

def init_dependencies(app: FastAPI) -> None:
    async_session = async_sessionmaker(async_engine, expire_on_commit=False)
    
    app.dependency_overrides[AsyncSession] = partial(get_async_session, async_session)
    # app.dependency_overrides[UsersService] = wrap_factory(UsersService)
    # app.dependency_overrides[UsersRepository] = wrap_factory(UsersRepository)
    # app.dependency_overrides[AuthService] = wrap_factory(AuthService)
    
    app.dependency_overrides[UsersService] = get_user_service
    app.dependency_overrides[UsersRepository] = get_user_repository
    app.dependency_overrides[AuthService] = get_auth_service
    app.dependency_overrides[SessionRedisHandler] = get_session_redis_handler
    # app.dependency_overrides[Hasher] = get_hasher
    
