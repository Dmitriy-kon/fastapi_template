from sqlalchemy.orm import mapped_column, Mapped

from .base import Base
from app.application.schemas.users import UserDTO

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    salt: Mapped[str] = mapped_column(nullable=False)
    
    def to_dto(self):
        data = {}
        for i in vars(self):
            if i != "_sa_instance_state":
                data[i] = getattr(self, i)
        
        dto = UserDTO(**data)
        return dto
    @classmethod
    def from_dto(cls, dto):
        return User(**dto.to_dict())
        # return UserDTO(
        #     id=self.id, 
        #     name=self.name, 
        #     hashed_password=self.hashed_password, 
        #     salt=self.salt
        #     created_at=self.created_at,
        #     updated_at=self.updated_at)