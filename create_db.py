import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('lms.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('user', 'admin')) NOT NULL DEFAULT 'user'
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    available INTEGER NOT NULL DEFAULT 1
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS borrowed (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER,
    borrow_date DATE,
    due_date DATE,
    returned INTEGER DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(book_id) REFERENCES books(id)
)
""")

# Insert admin
cur.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            ("Admin", "admin@lms.com", "Admin@123", "admin"))

# Insert 60 books
for i in range(1, 61):
    cur.execute("INSERT INTO books (title, author) VALUES (?, ?)", (f"Book Title {i}", f"Author {i}"))

conn.commit()
conn.close()

print("✅ lms.db created successfully!")
