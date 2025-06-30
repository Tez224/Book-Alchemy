from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    """
    Represents an author in the library database.
    Attributes:
        id (int): Primary key, auto-incremented.
        name (str): Full name of the author.
        birth_date (datetime): Date of birth.
        death_date (datetime or None): Date of death (nullable).
    """
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    death_date = db.Column(db.DateTime, nullable=True)

    def __str__(self):
        return f"{self.name} ({self.birth_date.date()} – {self.death_date.date()})"

    def __repr__(self):
        return f"<Author id={self.id} name='{self.name}'>"

class Book(db.Model):
    """
    Represents a book in the library database.

    Attributes:
        id (int): Primary key, auto-incremented.
        isbn (int): The book's ISBN number.
        title (str): Title of the book.
        publication_year (int): Year the book was published.
        author_id (int): Foreign key linking to the Author table.
        author (Author): SQLAlchemy relationship to the corresponding Author.
    """
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=True)

    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    author = db.relationship('Author', backref='books')

    def __str__(self):
        return f"'{self.title}' ({self.publication_year})"

    def __repr__(self):
        return f"<Book id={self.id} title='{self.title}' isbn={self.isbn}>"

