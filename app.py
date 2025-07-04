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

def get_cover_url(isbn):
    """
    Returns a cover image URL from Open Library based on the book's ISBN.
    :param isbn: The ISBN of the book.
    :return: A URL string pointing to the book cover image.
    """
    return f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"

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


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Displays and handles the form to add a new author.
    Accepts POST requests with author data and stores it in the database.
    """
    if request.method == 'POST':
        try:
            # Validate required fields
            if not request.form['name']:
                flash('Name is required!', 'error')
                return render_template('add_author.html')

            if not request.form['birthdate']:
                flash('Birth date is required!', 'error')
                return render_template('add_author.html')

            # Convert form input (strings) to datetime objects
            try:
                birth_date = datetime.strptime(request.form['birthdate'], '%Y-%m-%d')
            except ValueError:
                flash('Birth date format is invalid! Please use YYY-MM-DD', 'error')
                return render_template('add_author.html')

            death_date = None
            death_date_input = request.form.get('date_of_death', '')
            if death_date_input:
                try:
                    death_date = datetime.strptime(death_date_input, '%Y-%m-%d') if death_date_input else None
                except ValueError:
                    flash('Death date format is invalid! Please use YYYY-MM-DD or leave empty.', 'error')
                    return render_template('add_author.html')

            # Get new_data from form
            new_author = Author(
                name = request.form['name'],
                birth_date = birth_date,
                death_date = death_date,
            )

            # Add to the session and commit
            db.session.add(new_author)
            db.session.commit()

            flash('Author added successfully!', 'success')
            return render_template('add_author.html')

        except Exception as e:
            db.session.rollback()
            flash('An error occurred: {}'.format(e), 'error')

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Displays and handles the form to add a new book.
    Checks whether the author exists. If not, prompts user to add the author.
    Links the book to the correct author and saves it.
    """
    if request.method == 'POST':
        title = request.form['title']
        isbn = request.form['isbn']
        year = int(request.form['publication_year'])
        publication_year = year if year else None
        author_name = request.form['author_name'].strip()

        author = Author.query.filter_by(name=author_name).first()

        if not author:
            # Author not found — redirect to "add author" page
            message = f"Author '{author_name}' not found. Please add them first."
            return render_template('/add_author.html', message=message)

        # Author exists — create book linked to them
        new_book = Book(
            title=title,
            isbn=isbn,
            publication_year=publication_year,
            author=author
        )

        db.session.add(new_book)
        db.session.commit()

        print("Book added!")

    return render_template('add_book.html')


@app.route('/book/<int:book_id>', methods=['POST'])
def book(book_id):
    """
    Deletes a book from the database based on its ID.
    Shows a flash message and redirects to home.
    :param book_id: ID of the book to delete.
    """
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()

    flash(f"Book '{book.title}' was successfully deleted.")
    return redirect('/')


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
