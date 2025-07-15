from pydantic import BaseModel

class CategoryBase(BaseModel):
    description: str

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True
