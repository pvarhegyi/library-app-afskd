from pydantic import BaseModel, EmailStr


class BorrowerBase(BaseModel):
    name: str
    email: EmailStr


class BorrowerCreate(BorrowerBase):
    pass


class BorrowerResponse(BorrowerBase):
    id: int

    class Config:
        orm_mode = True
