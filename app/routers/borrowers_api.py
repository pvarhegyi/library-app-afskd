from typing import List

from db.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.borrower import BorrowerCreate, BorrowerResponse
from schemas.loan import LoanResponse
from services.borrower_service import BorrowerService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/borrowers", tags=["Borrowers"])


@router.post("/", response_model=BorrowerResponse, status_code=status.HTTP_201_CREATED)
def create_borrower(borrower: BorrowerCreate, db: Session = Depends(get_db)):
    return BorrowerService(db).create_borrower(borrower)


@router.get("/{borrower_id}", response_model=BorrowerResponse)
def get_borrower(borrower_id: int, db: Session = Depends(get_db)):
    borrower = BorrowerService(db).get_borrower(borrower_id)
    if not borrower:
        raise HTTPException(status_code=404, detail="Borrower not found")
    return borrower


@router.get("/{borrower_id}/books", response_model=List[LoanResponse])
def get_borrowed_books(borrower_id: int, db: Session = Depends(get_db)):
    return BorrowerService(db).get_borrowed_books(borrower_id)
