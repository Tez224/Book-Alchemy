# 📚 Flask Library Web App

A simple Flask-based web application to manage a personal library. Users can:

- Add authors and their birth/death dates  
- Add books with title, ISBN, and publication year  
- Link books to authors  
- Search and sort books  
- Delete books  
- Display book cover images via ISBN from the Open Library API  

---

## 🚀 Features

- Flask web framework  
- SQLAlchemy ORM with SQLite  
- Search and sort functionality  
- External book cover images  
- Safe deletion of books  
- Flash messages for user feedback  
- Clean MVC-style separation of concerns  

---

## 🛠 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Create a virtual environment and activate it

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> If you're using `.env`, also install `python-dotenv`:
```bash
pip install python-dotenv
```

---

### 4. Set environment variables

Create a `.env` file in the root directory and add:

```
SECRET_KEY=your_secret_key
```

Don't forget to add `.env` to your `.gitignore`.

---

### 5. Run the application

```bash
python app.py
```

Then open your browser and go to:  
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📁 Project Structure

```
├── app.py                 # Main application
├── data_models.py         # SQLAlchemy models
├── /templates             # HTML templates
│   ├── home.html
│   ├── add_book.html
│   └── add_author.html
├── /static                # Static assets (optional)
├── /data                  # SQLite database folder
│   └── library.sqlite
├── .env                   # Environment secrets
├── .gitignore
└── README.md
```

---

## 📷 Book Covers

Covers are fetched using ISBN via:  
`https://covers.openlibrary.org/b/isbn/<ISBN>-L.jpg`

Example in Python:

```python
def get_cover_url(isbn):
    return f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
```

---

## 🧾 License

MIT License – use, modify, and share freely.

---

