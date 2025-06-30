import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, flash
from data_models import db, Author, Book

# Get the absolute path to the 'data' folder
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'data', 'library.sqlite')

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Use the absolute database path
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{database_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/', methods=['GET'])
def index():
    """
    Displays the home page with a list of books.
    Allows filtering by search term and sorting by title, author, or year.
    """
    search_term = request.args.get('search', '').strip()
    sort_by = request.args.get('sort', 'title')  # default = title

    query = Book.query

    if search_term:
        query = query.filter(Book.title.ilike(f"%{search_term}%"))

    if sort_by == 'year':
        query = query.order_by(Book.publication_year)
    elif sort_by == 'author':
        query = query.join(Book.author).order_by(Author.name)
    else:
        query = query.order_by(Book.title)

    books = query.all()

    return render_template('home.html', books=books, search=search_term, sort_by=sort_by)


if __name__ == '__main__':
    """
    Initializes the database and starts the Flask app.
    Ensures the 'data/' directory exists before running.
    """
    # Ensure the 'data/' folder really exists at runtime
    os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)

    #with app.app_context():
        #db.create_all()
        #print(Author.__table__)
        #print(Book.__table__)
        #print("Database and tables created.")
    app.run(debug=True)
