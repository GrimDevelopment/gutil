from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class User(BaseModel):
    id: UUID
    email: str
    username: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True