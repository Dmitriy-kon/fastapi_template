from pydantic import BaseModel

from app.application.dto.users import UserDTO


class SUser(BaseModel):
    name: str

class SUserIn(BaseModel):
    name: str
    password: str
    
    def to_dto(self):
        return UserDTO(
            name=self.name, 
            hashed_password=self.password,
            # salt="123"
           )