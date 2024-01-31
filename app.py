from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Book
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/p/Desktop/Ai_Dev/Python forts/Books/books_db.db'
db = SQLAlchemy(app)
db.init_app(app) 

@app.route('/')
def hello_world():
    return 'Hej Världen!'

# Define the Book model
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    summary = db.Column(db.String)
    genre = db.Column(db.String, nullable=False)
    reviews = db.relationship('Review', backref='book', lazy=True)

    def __repr__(self):
        return f'<Book {self.title}>'

# Define the Review model
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<Review {self.id} for Book {self.book_id}>'

# Add a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    print(data)
    new_book = Book(title=data['title'], author=data['author'], summary=data['summary'], genre=data['genre'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 201

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = [{'id': book.id, 'title': book.title, 'author': book.author, 'summary': book.summary, 'genre': book.genre} for book in books]
    return jsonify({'books': book_list})

# Update a book
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    book = Book.query.get_or_404(id)
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.summary = data.get('summary', book.summary)
    book.genre = data.get('genre', book.genre)
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'})

# Delete a book
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})

# Add a review for a book
@app.route('/books/<int:book_id>/reviews', methods=['POST'])
def add_review(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    new_review = Review(book_id=book.id, rating=data['rating'], comment=data.get('comment', ''))
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'message': 'Review added successfully'}), 201

# Get all reviews for a specific book
@app.route('/books/<int:book_id>/reviews', methods=['GET'])
def get_reviews(book_id):
    reviews = Review.query.filter_by(book_id=book_id).all()
    review_list = [{'id': review.id, 'rating': review.rating, 'comment': review.comment} for review in reviews]
    return jsonify({'reviews': review_list})

# Update a review
@app.route('/reviews/<int:id>', methods=['PUT'])
def update_review(id):
    data = request.get_json()
    review = Review.query.get_or_404(id)
    review.rating = data.get('rating', review.rating)
    review.comment = data.get('comment', review.comment)
    db.session.commit()
    return jsonify({'message': 'Review updated successfully'})

# Delete a review
@app.route('/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    review = Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted successfully'})

#Top review
@app.route('/books/top', methods=['GET'])
def top_rated_books():
    top_books = db.session.query(
        Book.title, Book.author, func.avg(Review.rating).label('average_rating')
    ).join(Review).group_by(Book.id).order_by(func.avg(Review.rating).desc()).limit(5).all()

    top_books_list = [{'title': book.title, 'author': book.author, 'average_rating': round(book.average_rating, 2)} for book in top_books]
    
    return jsonify({'top_books': top_books_list})

@app.route('/author', methods=['GET'])
def get_author_info():
    author_name = request.args.get('name')
    if not author_name:
        return jsonify({'error': 'No author name provided'}), 400

    try:
        # Make a request to the Open Library API
        response = requests.get(f'https://openlibrary.org/search/authors.json?q={author_name}')
        if response.status_code == 200:
            author_data = response.json() 
            # Call a function to extract summary and famous works (you need to implement this)
            summary, works = extract_author_data(author_data)
            return jsonify({'summary': summary, 'famous_works': works})
        else:
            # If the API request was not successful, return an error
            return jsonify({'error': 'Failed to fetch data from external API'}), 500
    except requests.RequestException as e:
        # If there was an error during the request (like a network problem), return an error
        return jsonify({'error': str(e)}), 500

def extract_author_data(author_data):
    if 'docs' in author_data and len(author_data['docs']) > 0:
        first_author = author_data['docs'][0]  

        # Extract the author's biography as the summary
        # If no biography is provided, use a default message
        summary = first_author.get('bio', 'No biography available')

        # Extract the author's most famous work
        # If no top work is provided, use a default message
        top_work = first_author.get('top_work', 'No top work available')

        return summary, top_work
    else:
        # Return default values if no author data is found
        return "No author information available", "No top work available"


if __name__ == '__main__':
    app.run(debug=True)
