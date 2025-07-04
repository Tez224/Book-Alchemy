# init_db.py
from app import app, db, basedir
import os

def initialize_database():
    """Initialize the database and create tables"""
    with app.app_context():
        os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)
        db.create_all()
        print("Database tables created:")
        print(db.metadata.tables.keys())

if __name__ == '__main__':
    initialize_database()