from typing import Annotated


from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, insert

from app.adapters.sqlalchemyDb.models import User
from app.api.depends_stub import Stub
from app.application.dto.users import UserDTO


class UsersRepository:
    def __init__(
        self, session: Annotated[AsyncSession, Depends(Stub(AsyncSession))]
    ) -> None:
        self.session = session
        self.model = User

    async def get_all_users(self) -> list[UserDTO]:
        stmt = select(self.model).order_by(self.model.id)
        res = await self.session.execute(stmt)
        res = res.scalars().all()

        res = [i.to_dto() for i in res]
        return res

    async def get_user_by_id(self, user_id) -> UserDTO:
        stmt = select(self.model).where(self.model.id == user_id)
        res = await self.session.execute(stmt)
        res = res.scalars().one()

        res = res.to_dto()
        return res

    async def get_user_by_name(self, name) -> UserDTO:
        stmt = select(self.model).where(self.model.name == name)
        res = await self.session.execute(stmt)
        res = res.scalars().one()

        res = res.to_dto()
        return res

    async def create_user(self, user: UserDTO) -> UserDTO:
        # user = User.from_dto(user)
        stmt = insert(self.model).values(**user.to_dict()).returning(self.model)
        await self.session.execute(stmt)
        return user

    async def commit(self):
        return await self.session.commit()
