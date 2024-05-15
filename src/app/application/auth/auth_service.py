from fastapi import HTTPException, Request


from .hash_password import hash_password, compare_passwords

from app.application.services.users import UsersService
from app.application.dto.users import UserDTO

from app.adapters.redisDb.redis_gateway import SessionRedisHandler




class AuthService:
    def __init__(self, 
                 user_service: UsersService,
                 session_handler: SessionRedisHandler) -> None:
        self.user_service = user_service
        self.session_handler = session_handler

    def register_user(self, user: UserDTO) -> UserDTO:
        hashed_password = hash_password(user.hashed_password)
        user.hashed_password = hashed_password.decode()

        res = self.user_service.create_user(user)
        return res

    async def login_user(
        self, 
        user: UserDTO,
        request: Request) -> None:
        user_in_db = await self.user_service.get_user_by_name(user.name)

        res = compare_passwords(
            user.hashed_password, user_in_db.hashed_password.encode()
        )
        
        if res:
            session_id = request.cookies.get("session_id")
            session_res = None
            
            print(f"{session_id=}")
            
            if session_id:
                session_res = await self.session_handler.get_session(session_id)
                
            print(f"{session_res=}")
            
            if session_res:
                await self.session_handler.delete_session(session_id)

            session_id = await self.session_handler.create_session(user_in_db.name)

            return session_id

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    async def get_session(self, session_id: str) -> str:
        return await self.session_handler.get_session(session_id)

