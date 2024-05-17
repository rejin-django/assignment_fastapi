# Book Review API

This project implements a RESTful API for a hypothetical book review system using FastAPI. The API allows users to add books, submit reviews, retrieve books, and retrieve reviews for specific books. It also integrates with an SQLite database and includes background task processing and testing.

## Setup

### Prerequisites

- Python 3.7+
- `pip` (Python package installer)

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/book_review_api.git
   cd book_review_api
2.Create and activate a virtual environment:
  python -m venv env
  source env/bin/activate
3.Install dependencies:
pip install -r requirements.txt
4.Run the application:
uvicorn main:app --reload
The API will be available at http://127.0.0.1:8000.

API Endpoints:
Books
Add a new book
POST /books/
Request Body:
json
{
  "title": "Book Title",
  "author": "Author Name",
  "publication_year": 2020
}
Response:

json
{
  "id": 1,
  "title": "Book Title",
  "author": "Author Name",
  "publication_year": 2020
}

Retrieve all books with optional filtering by author or year
GET /books/
Query Parameters:

author (optional)
year (optional)
Response:

json
[
{
"id": 1,
"title": "Book Title",
"author": "Author Name",
"publication_year": 2020
}
]

Reviews
Submit a review for a book
POST /reviews/
Request Body:

json
{
  "book_id": 1,
  "text": "Great book!",
  "rating": 5
}

Response:

json
{
  "id": 1,
  "book_id": 1,
  "text": "Great book!",
  "rating": 5
}
Retrieve all reviews for a specific book

GET /reviews/{book_id}
Response:

json

[
  {
    "id": 1,
    "book_id": 1,
    "text": "Great book!",
    "rating": 5
  }
]

Background Task
The API includes a background task to simulate sending a confirmation email when a review is posted. This is handled using FastAPI's BackgroundTasks.

Testing
To run the tests, use:
pytest
The tests cover the basic CRUD operations for books and reviews and ensure the endpoints are functioning correctly.

License
This project is licensed under the MIT License. See the LICENSE file for details.
