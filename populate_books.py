import sqlite3

# 30 real books (you can replace with your favorites)
books = [
    ("To Kill a Mockingbird", "Harper Lee"),
    ("1984", "George Orwell"),
    ("Pride and Prejudice", "Jane Austen"),
    ("The Great Gatsby", "F. Scott Fitzgerald"),
    ("The Catcher in the Rye", "J.D. Salinger"),
    ("The Hobbit", "J.R.R. Tolkien"),
    ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling"),
    ("Fahrenheit 451", "Ray Bradbury"),
    ("Moby Dick", "Herman Melville"),
    ("The Lord of the Rings", "J.R.R. Tolkien"),
    ("Jane Eyre", "Charlotte Brontë"),
    ("Animal Farm", "George Orwell"),
    ("Brave New World", "Aldous Huxley"),
    ("The Chronicles of Narnia", "C.S. Lewis"),
    ("Crime and Punishment", "Fyodor Dostoevsky"),
    ("The Kite Runner", "Khaled Hosseini"),
    ("The Alchemist", "Paulo Coelho"),
    ("The Da Vinci Code", "Dan Brown"),
    ("A Tale of Two Cities", "Charles Dickens"),
    ("Wuthering Heights", "Emily Brontë"),
    ("Les Misérables", "Victor Hugo"),
    ("Gone with the Wind", "Margaret Mitchell"),
    ("The Shining", "Stephen King"),
    ("Life of Pi", "Yann Martel"),
    ("The Girl on the Train", "Paula Hawkins"),
    ("The Book Thief", "Markus Zusak"),
    ("The Hunger Games", "Suzanne Collins"),
    ("Twilight", "Stephenie Meyer"),
    ("Percy Jackson & the Olympians", "Rick Riordan"),
    ("The Fault in Our Stars", "John Green")
]

try:
    conn = sqlite3.connect("lms.db")
    cur = conn.cursor()

    for title, author in books:
        cur.execute("INSERT INTO books (title, author, available) VALUES (?, ?, 1)", (title, author))

    conn.commit()
    print("✅ Books inserted successfully into 'books' table.")

except Exception as e:
    print("❌ Error:", e)

finally:
    conn.close()
