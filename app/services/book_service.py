from fastapi import HTTPException
from models.book import Book
from models.borrower import Borrower
from models.loan import Loan
from opentelemetry import metrics, trace
from schemas.book import BookCreate
from sqlalchemy.orm import Session
import time

tracer = trace.get_tracer("books.tracer")

meter = metrics.get_meter("library-api")

borrow_duration_histogram = meter.create_histogram(
    name="borrow_book_duration",
    unit="ms",
    description="Duration of borrow_book operation"
)

borrow_fail_counter = meter.create_counter(
    name="borrow_failures_total",
    description="Total number of failed borrow attempts"
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
        """Add a new book to the database.
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
            start = time.time()
            book = self.db.query(Book).filter(Book.id == book_id).first()
            borrower = (
                self.db.query(Borrower).filter(Borrower.id == borrower_id).first()
            )
            if not borrower:
                borrow_span.set_attribute("error", True)
                borrow_fail_counter.add(1)
                raise HTTPException(status_code=404, detail="Borrower not found")
            if not book:
                borrow_span.set_attribute("error", True)
                borrow_fail_counter.add(1)
                raise HTTPException(status_code=404, detail="Book not found")
            if not book.available:
                borrow_span.set_attribute("already_borrowed", True)
                borrow_fail_counter.add(1)
                raise HTTPException(status_code=400, detail="Book not available")
            book.available = False
            loan = Loan(borrower_id=borrower_id, book_id=book.id)
            self.db.add(loan)
            self.db.commit()
            end = time.time()
            duration = (end - start) * 1000
            borrow_duration_histogram.record(duration)
            return loan
