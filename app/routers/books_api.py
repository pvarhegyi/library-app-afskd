from fastapi import APIRouter, Depends, HTTPException, status
import pytest
from sqlalchemy.orm import Session
from db.database import get_db
from models.base import Base
from schemas.book import BookCreate, BookResponse
from schemas.loan import LoanResponse
from services.book_service import BookService
from typing import List

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[BookResponse])
def list_books(db: Session = Depends(get_db)):
    return BookService(db).list_books()


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    return BookService(db).add_book(book)


@router.post(
    "/{book_id}/borrow",
    response_model=LoanResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Book not found"},
        status.HTTP_400_BAD_REQUEST: {"description": "Book already borrowed"},
    },
)
def borrow_book(book_id: int, borrower_id: int, db: Session = Depends(get_db)):
    service = BookService(db)
    loan = service.borrow_book(book_id, borrower_id)
    return loan
