# main.py
from fastapi import FastAPI, HTTPException, Depends,BackgroundTasks
from pydantic import BaseModel, Field
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from typing import List, Optional
from models import books, reviews
from database import DATABASE_URL, metadata

app = FastAPI()

# Database setup
engine = create_engine(DATABASE_URL)
metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
class Book(BaseModel):
    title: str
    author: str
    publication_year: int

class Review(BaseModel):
    book_id: int
    text: str
    rating: int = Field(..., ge=1, le=5)

class BookInDB(Book):
    id: int

class ReviewInDB(Review):
    id: int

# CRUD operations
@app.post("/books/", response_model=BookInDB)
async def add_book(book: Book, db: Session = Depends(get_db)):
    db_book = books.insert().values(**book.dict())
    result = db.execute(db_book)
    db.commit()
    return {**book.dict(), "id": result.lastrowid}

def send_confirmation_email(review: ReviewInDB):
    # Simulate sending an email
    print(f"Sending confirmation email for review: {review.id}")

@app.post("/reviews/", response_model=ReviewInDB)
async def add_review(review: Review, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_review = reviews.insert().values(**review.dict())
    result = db.execute(db_review)
    db.commit()
    review_in_db = {**review.dict(), "id": result.lastrowid}
    background_tasks.add_task(send_confirmation_email, ReviewInDB(**review_in_db))
    return review_in_db

@app.get("/books/", response_model=List[BookInDB])
async def get_books(author: Optional[str] = None, year: Optional[int] = None, db: Session = Depends(get_db)):
    query = books.select()
    if author:
        query = query.where(books.c.author == author)
    if year:
        query = query.where(books.c.publication_year == year)
    result = db.execute(query)
    return [BookInDB(**row) for row in result.fetchall()]

@app.get("/reviews/{book_id}", response_model=List[ReviewInDB])
async def get_reviews(book_id: int, db: Session = Depends(get_db)):
    query = reviews.select().where(reviews.c.book_id == book_id)
    result = db.execute(query)
    return [ReviewInDB(**row) for row in result.fetchall()]


