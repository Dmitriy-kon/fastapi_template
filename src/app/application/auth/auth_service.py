


from app.application.services.users import UsersService
from .hash_password import hash_password, compare_passwords
from app.application.dto.users import UserDTO


class AuthService:
    def __init__(
        self,
        user_service: UsersService) -> None:
        self.user_service = user_service

    def register_user(self, user: UserDTO) -> UserDTO:
        hashed_password = hash_password(user.hashed_password)
        user.hashed_password = hashed_password.decode()
        
        res = self.user_service.create_user(user)
        return res

    def login_user(self, name: str, password: str) -> None:
        pass