import pytest
from db.database import get_db
from fastapi.testclient import TestClient
from main import app
from models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
import os


@pytest.fixture
def db_session(scope="function"):
    """Create a new database session for a test. Initializes the database and cleans up after the test."""
    if os.path.exists(TEST_DATABASE_URL):
        os.remove(TEST_DATABASE_URL)

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        if os.path.exists(TEST_DATABASE_URL):
            os.remove(TEST_DATABASE_URL)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    from fastapi.testclient import TestClient

    client = TestClient(app)
    yield client


def test_add_list_books(client):
    response = client.post(
        "/api/books/", json={"title": "1984", "author": "George Orwell"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "1984"
    assert response.json()["author"] == "George Orwell"

    response = client.get("/api/books/")
    assert response.status_code == 200
    assert response.json()[0]["title"] == "1984"
    assert response.json()[0]["author"] == "George Orwell"


def test_borrow_existing_book(client):
    response = client.post(
        "/api/borrowers/", json={"name": "Alice", "email": "alice@alice.com"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Alice"
    borrower_id = response.json()["id"]

    response = client.post(
        "/api/books/", json={"title": "1984", "author": "George Orwell"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "1984"
    book_id = response.json()["id"]

    response = client.post(
        f"/api/books/{book_id}/borrow/", params={"borrower_id": borrower_id}
    )
    assert response.status_code == 200


def test_borrow_nonexisting_book(client):
    response = client.post(
        "/api/borrowers/", json={"name": "Alice", "email": "alice@alice.com"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Alice"
    borrower_id = response.json()["id"]

    response = client.post(
        "/api/books/99999/borrow/", params={"borrower_id": borrower_id}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"
