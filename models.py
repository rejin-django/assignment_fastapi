# models.py
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from database import metadata

books = Table(
    "books",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("title", String, index=True),
    Column("author", String, index=True),
    Column("publication_year", Integer),
)

reviews = Table(
    "reviews",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("book_id", Integer, ForeignKey("books.id")),
    Column("text", String),
    Column("rating", Integer),
)
