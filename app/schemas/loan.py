from datetime import datetime

from pydantic import BaseModel


class LoanBase(BaseModel):
    book_id: int
    borrower_id: int


class LoanCreate(LoanBase):
    pass


class LoanResponse(LoanBase):
    id: int
    borrowed_at: datetime

    class Config:
        orm_mode = True
