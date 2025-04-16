from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from models.book import Book
from models.borrower import Borrower
from models.loan import Loan
from services.book_service import BookService
from sqlalchemy.orm import Session


def test_borrow_book_success():
    mock_db = MagicMock(spec=Session)

    mock_book = Book(
        id=1, title="Alice in Wonderland", author="Lewis Caroll", available=True
    )
    mock_borrower = Borrower(id=1, name="Carol", email="carol@example.com")
    mock_db.query.return_value.filter.return_value.first.side_effect = [
        mock_book,
        mock_borrower,
    ]

    service = BookService(mock_db)

    loan = service.borrow_book(book_id=1, borrower_id=1)

    assert loan.book_id == 1
    assert loan.borrower_id == 1
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    assert not mock_book.available


def test_borrow_book_book_not_found():
    mock_db = MagicMock(spec=Session)
    mock_borrower = Borrower(id=1, name="Bob", email="bob@example.com")
    mock_db.query.return_value.filter.return_value.first.side_effect = [
        None,
        mock_borrower,
    ]
    service = BookService(mock_db)

    with pytest.raises(HTTPException) as exc_info:
        service.borrow_book(book_id=1, borrower_id=1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Book not found"


def test_borrow_book_borrower_not_found():
    mock_db = MagicMock(spec=Session)
    mock_book = Book(
        id=1, title="Winnie-the-Pooh", author="A. A. Milne", available=True
    )
    mock_db.query.return_value.filter.return_value.first.side_effect = [mock_book, None]
    service = BookService(mock_db)

    with pytest.raises(HTTPException) as exc_info:
        service.borrow_book(book_id=1, borrower_id=1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Borrower not found"


def test_borrow_book_already_borrowed():
    mock_db = MagicMock(spec=Session)
    mock_book = Book(
        id=1, title="Pride and Prejudice", author="Jane Austen", available=False
    )
    mock_borrower = Borrower(id=1, name="Jane", email="jane@example.com")
    mock_db.query.return_value.filter.return_value.first.side_effect = [
        mock_book,
        mock_borrower,
    ]
    service = BookService(mock_db)
    with pytest.raises(HTTPException) as exc_info:
        service.borrow_book(book_id=1, borrower_id=1)

    # Assertions
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Book not available"
