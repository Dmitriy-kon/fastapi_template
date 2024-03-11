from datetime import datetime
from dataclasses import dataclass, asdict, field


@dataclass
class UserDTO:
    name: str
    hashed_password: str
    # salt: str | None
    id: int | None = field(default=None)
    created_at: datetime | None = field(default=None)
    updated_at: datetime | None = field(default=None)
    
    def to_dict(self):
        return {i: j for i, j in asdict(self).items() if j}