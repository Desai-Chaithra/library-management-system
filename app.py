from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Home
@app.route('/')
def index():
    return render_template('index.html')

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        if len(password) < 6:
            return "Password must be at least 6 characters long."

        con = sqlite3.connect('lms.db')
        cur = con.cursor()
        cur.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)", (name, email, password, role))
        con.commit()
        con.close()

        return redirect(url_for('login'))
    return render_template('signup.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        con = sqlite3.connect('lms.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cur.fetchone()
        con.close()

        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            error = "Invalid credentials."
    return render_template('login.html', error=error)

# Admin Dashboard
@app.route('/admin')
def admin_dashboard():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    con = sqlite3.connect('lms.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    books = cur.execute("SELECT * FROM books").fetchall()
    con.close()

    return render_template('admin.html', books=books)

# User Dashboard
@app.route('/dashboard')
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    con = sqlite3.connect('lms.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    books = cur.execute("SELECT * FROM books WHERE available = 1").fetchall()

    borrowed = cur.execute("""
        SELECT b.id, b.book_id, bk.title, bk.author, b.borrow_date, b.due_date
        FROM borrowed b
        JOIN books bk ON b.book_id = bk.id
        WHERE b.user_id = ?
    """, (session['user_id'],)).fetchall()

    con.close()
    return render_template('dashboard.html', books=books, borrowed=borrowed)

# Check Borrow Limit
@app.route('/borrow_check')
def borrow_check():
    if 'user_id' not in session:
        return jsonify({'allowed': False, 'message': 'You must be logged in.'})

    con = sqlite3.connect('lms.db')
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM borrowed WHERE user_id = ?", (session['user_id'],))
    count = cur.fetchone()[0]
    con.close()

    if count >= 4:
        return jsonify({'allowed': False, 'message': 'You have already borrowed 4 books. Please return some before borrowing more.'})
    return jsonify({'allowed': True})

# Borrow Book
@app.route('/borrow/<int:book_id>')
def borrow_book(book_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    con = sqlite3.connect('lms.db')
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM borrowed WHERE user_id = ?", (session['user_id'],))
    count = cur.fetchone()[0]
    if count >= 4:
        con.close()
        return "Borrow limit exceeded. Return books to borrow new ones."

    borrow_date = datetime.now().strftime('%Y-%m-%d')
    due_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    cur.execute("INSERT INTO borrowed (user_id, book_id, borrow_date, due_date) VALUES (?, ?, ?, ?)", (session['user_id'], book_id, borrow_date, due_date))
    cur.execute("UPDATE books SET available = 0 WHERE id = ?", (book_id,))
    con.commit()
    con.close()
    return redirect(url_for('user_dashboard'))

# Return Book
@app.route('/return/<int:borrow_id>')
def return_book(borrow_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    con = sqlite3.connect('lms.db')
    cur = con.cursor()

    cur.execute("SELECT book_id FROM borrowed WHERE id = ?", (borrow_id,))
    result = cur.fetchone()
    if result:
        book_id = result[0]
        cur.execute("UPDATE books SET available = 1 WHERE id = ?", (book_id,))
        cur.execute("DELETE FROM borrowed WHERE id = ?", (borrow_id,))
        con.commit()

    con.close()
    return redirect(url_for('user_dashboard'))

# ✅ Logout redirects to index now
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
