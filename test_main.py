import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import metadata
from main import app, get_db
from models import books, reviews

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_db():
    metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

def test_add_book(client):
    response = client.post("/books/", json={"title": "Book Title", "author": "Author", "publication_year": 2020})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Book Title"
    assert data["author"] == "Author"
    assert data["publication_year"] == 2020
    assert "id" in data

def test_add_review(client):
    response = client.post("/reviews/", json={"book_id": 1, "text": "Great book!", "rating": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == 1
    assert data["text"] == "Great book!"
    assert data["rating"] == 5
    assert "id" in data

def test_get_books(client):
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_get_reviews(client):
    response = client.get("/reviews/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
