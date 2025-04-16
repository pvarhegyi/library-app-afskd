from fastapi import HTTPException
from models.borrower import Borrower
from models.loan import Loan
from schemas.borrower import BorrowerCreate
from sqlalchemy.orm import Session


class BorrowerService:
    def __init__(self, db: Session):
        self.db = db

    def create_borrower(self, borrower_data: BorrowerCreate) -> Borrower:
        """Create a new borrower in the database.
        Args:
            borrower_data (BorrowerCreate): The borrower data to be added.
        Returns:
            Borrower: The created borrower object.
        """
        borrower = Borrower(**borrower_data.model_dump())
        self.db.add(borrower)
        self.db.commit()
        self.db.refresh(borrower)
        return borrower

    def get_borrower(self, borrower_id: int) -> Borrower | None:
        """Get a borrower by ID.
        Args:
            borrower_id (int): The ID of the borrower to retrieve.
        Returns:
            Borrower: The borrower object if found, None otherwise.
        """
        borrower = self.db.query(Borrower).filter(Borrower.id == borrower_id).first()
        if not borrower:
            raise HTTPException(status_code=404, detail="Borrower not found")
        return borrower

    def get_borrowed_books(self, borrower_id: int) -> list[Loan]:
        """Get all books borrowed by a borrower.
        Args:
            borrower_id (int): The ID of the borrower.
        Returns:
            list[Loan]: A list of loan objects associated with the borrower.
        """
        borrower = self.db.query(Borrower).filter(Borrower.id == borrower_id).first()
        if not borrower:
            raise HTTPException(status_code=404, detail="Borrower not found")
        return self.db.query(Loan).filter(Loan.borrower_id == borrower_id).all()
