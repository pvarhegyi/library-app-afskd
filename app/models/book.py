from models.base import Base
from sqlalchemy import Boolean, Column, Integer, String


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    available = Column(Boolean, default=True)
