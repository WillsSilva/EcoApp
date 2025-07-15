from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    name: str
    cpf: str
    phone_number: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    create_at: datetime
    is_active: bool

    class Config:
        orm_mode = True
