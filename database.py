import sqlite3

def connect_db():
    return sqlite3.connect("books.db")

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def insert_book(title, author, year):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
    conn.commit()
    conn.close()

def update_book(book_id, title, author, year):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title=?, author=?, year=? WHERE id=?", (title, author, year, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

def fetch_books():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()
    return rows