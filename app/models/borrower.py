# models/borrower.py
from models.base import Base
from sqlalchemy import Column, Integer, String


class Borrower(Base):
    __tablename__ = "borrowers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
