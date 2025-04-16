from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.book import Book
from models.borrower import Borrower
from models.loan import Loan
from schemas.book import BookCreate
from opentelemetry import trace, metrics

tracer = trace.get_tracer("books.tracer")

meter = metrics.get_meter("library-api")
loan_counter = meter.create_counter(
    name="loaned_books_total", description="Number of books loaned", unit="1"
)


class BookService:
    def __init__(self, db: Session):
        self.db = db

    def list_books(self) -> list[Book]:
        """List all books in the database.
        Returns:
            list[Book]: A list of all book objects.
        """
        return self.db.query(Book).all()

    def add_book(self, book_data: BookCreate) -> Book:
        """ Add a new book to the database.
        Args:
            book_data (BookCreate): The book data to be added.
        Returns:
            Book: The created book object.
        """
        book = Book(**book_data.model_dump())
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def borrow_book(self, book_id: int, borrower_id: int) -> Loan:
        """Borrow a book by its ID and associate it with a borrower.
        Args:
            book_id (int): The ID of the book to borrow.
            borrower_id (int): The ID of the borrower.
        Returns:
            Loan: The created loan object if successful, None otherwise.
        Raises:
            HTTPException: If the book is not found or already borrowed.
        """
        with tracer.start_as_current_span("borrow") as borrow_span:
            borrow_span.set_attribute("book.id", book_id)
            borrow_span.set_attribute("borrower.id", borrower_id)

            loan_counter.add(1, {"book_id": book_id, borrower_id: borrower_id})

            book = self.db.query(Book).filter(Book.id == book_id).first()
            borrower = self.db.query(Borrower).filter(Borrower.id == borrower_id).first()
            if not borrower:
                borrow_span.set_attribute("error", True)
                raise HTTPException(status_code=404, detail="Borrower not found")
            if not book:
                borrow_span.set_attribute("error", True)
                raise HTTPException(status_code=404, detail="Book not found")
            if not book.available:
                borrow_span.set_attribute("already_borrowed", True)
                raise HTTPException(status_code=400, detail="Book not available")
            book.available = False
            loan = Loan(borrower_id=borrower_id, book_id=book.id)
            self.db.add(loan)
            self.db.commit()
            return loan
