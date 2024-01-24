import json
import pytest
from app import app, db
from models import Book, Review

@pytest.fixture
def client():
    # Setting up a test client for Flask application.
    # This configuration uses an in-memory database for tests.
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    # Setting up database before each test.
    with app.app_context():
        db.create_all()

    # Yielding client for testing.
    yield client

    # Teardown: Dropping the database after each test.
    with app.app_context():
        db.drop_all()

def test_add_book(client):
    # Test case for adding a new book to the database.
    new_book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "summary": "Test Summary",
        "genre": "Test Genre"
    }
    # Sending POST request to add a new book and capturing the response.
    response = client.post('/books', data=json.dumps(new_book_data), content_type='application/json')

    # Assertions to check if the book was added successfully.
    assert response.status_code == 201
    assert 'Book added successfully' in response.get_data(as_text=True)

def test_get_books(client):
    # Adding a book first to ensure the database is not empty.
    test_add_book(client)
    
    # Sending GET request to retrieve all books and capturing the response.
    response = client.get('/books')

    # Assertions to check if the response contains the book added earlier.
    assert response.status_code == 200
    assert 'Test Book' in response.get_data(as_text=True)

def test_add_review(client):
    # Adding a book first to ensure there's a book to attach the review to.
    test_add_book(client)

    # Data for the new review to be added.
    new_review_data = {
        "book_id": 1,  # Assuming the first book added has id 1
        "rating": 5,
        "comment": "Great book!"
    }
    # Sending POST request to add a review and capturing the response.
    response = client.post('/books/1/reviews', data=json.dumps(new_review_data), content_type='application/json')

    # Assertions to check if the review was added successfully.
    assert response.status_code == 201
    assert 'Review added successfully' in response.get_data(as_text=True)

def test_get_reviews(client):
    # Adding a book and a review first to ensure there's data to retrieve.
    test_add_review(client)

    # Sending GET request to retrieve reviews of the book and capturing the response.
    response = client.get('/books/1/reviews')

    # Assertions to check if the response contains the review added earlier.
    assert response.status_code == 200
    assert 'Great book!' in response.get_data(as_text=True)
