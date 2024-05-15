from typing import Annotated


from sqlalchemy.exc import NoResultFound, IntegrityError

from fastapi import Depends, HTTPException


from app.api.depends_stub import Stub
from app.application.dto.users import UserDTO
from app.application.repositories.users_rep import UsersRepository


class UsersService:
    def __init__(
        self, 
        repo: UsersRepository
        
    ) -> None:
        self.repo = repo

    async def get_all_users(self) -> list[UserDTO]:
        return await self.repo.get_all_users()

    async def get_user_by_id(self, id: int) -> UserDTO:
        try:
            return await self.repo.get_user_by_id(id)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="User not found")

    async def get_user_by_name(self, name: str) -> UserDTO:
        try:
            return await self.repo.get_user_by_name(name)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="User not found")

    async def create_user(self, user: UserDTO) -> UserDTO:
        try:
            res = await self.repo.create_user(user)
            await self.repo.commit()
            return res
        except IntegrityError:
            raise HTTPException(
                status_code=409, detail="User with this name already exists"
            )
