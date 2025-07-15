from pydantic import BaseModel
from datetime import datetime

class IncomeBase(BaseModel):
    id_user: int
    value: float
    source: str
    description: str

class IncomeCreate(IncomeBase):
    received_at: datetime

class IncomeOut(IncomeBase):
    id: int
    received_at: datetime

    class Config:
        orm_mode = True
