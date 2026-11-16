import os
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
import pymysql.cursors
import bcrypt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'super_secret_key')

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'registration'),
        cursorclass=pymysql.cursors.DictCursor
    )

def get_library_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database='library',
        cursorclass=pymysql.cursors.DictCursor
    )

# ==========================================
# TODO & AUTHENTICATION ROUTES
# ==========================================

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    filter_type = request.args.get('filter', 'all')
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS open_count FROM todos WHERE user_id = %s AND is_done = FALSE", (session['user_id'],))
            open_count_result = cursor.fetchone()
            open_count = open_count_result['open_count'] if open_count_result else 0

            if filter_type == 'active':
                sql = "SELECT todo_id, title, is_done, created_at FROM todos WHERE user_id = %s AND is_done = FALSE ORDER BY todo_id DESC"
            elif filter_type == 'completed':
                sql = "SELECT todo_id, title, is_done, created_at FROM todos WHERE user_id = %s AND is_done = TRUE ORDER BY todo_id DESC"
            else:
                sql = "SELECT todo_id, title, is_done, created_at FROM todos WHERE user_id = %s ORDER BY todo_id DESC"
                
            cursor.execute(sql, (session['user_id'],))
            todos = cursor.fetchall()
            return render_template('index.html', name=session['name'], todos=todos, current_filter=filter_type, open_count=open_count)
    finally:
        conn.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not name or not email or not password or not confirm_password:
            return render_template('register.html', error="All fields are required")
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match")

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)", (email, name, hashed_pw))
                conn.commit()
                session['user_id'] = cursor.lastrowid
                session['name'] = name
                return redirect(url_for('index'))
        except pymysql.MySQLError as e:
            if e.args[0] == 1062:
                return render_template('register.html', error="Email Already Exists")
            return render_template('register.html', error="Database error occurred")
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            return render_template('login.html', error="Email and password are required")
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT user_id, name, password_hash FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()
                if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                    session['user_id'] = user['user_id']
                    session['name'] = user['name']
                    return redirect(url_for('index'))
                return render_template('login.html', error="Invalid email or password")
        finally:
            conn.close()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_todo():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    title = request.form.get('title', '').strip()
    if not title:
        flash("Title is required")
        return redirect(url_for('index'))
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO todos (user_id, title) VALUES (%s, %s)", (session['user_id'], title))
            conn.commit()
    finally:
        conn.close()
    return redirect(url_for('index'))

@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle_todo(todo_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE todos SET is_done = NOT is_done WHERE todo_id = %s AND user_id = %s", (todo_id, session['user_id']))
            conn.commit()
    finally:
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM todos WHERE todo_id = %s AND user_id = %s", (todo_id, session['user_id']))
            conn.commit()
    finally:
        conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['POST'])
def edit_todo(todo_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    new_title = request.form.get('title', '').strip()
    if not new_title:
        flash('Title is required')
        return redirect(url_for('index'))
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE todos SET title = %s WHERE todo_id = %s AND user_id = %s", (new_title, todo_id, session['user_id']))
            conn.commit()
    finally:
        conn.close()
    return redirect(url_for('index'))


# ==========================================
# LIBRARY SYSTEM: F2.2 CATALOGUE + CRUD
# ==========================================

@app.route('/books')
def list_books():
    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT b.*, a.name AS author_name, p.name AS publisher_name, c.name AS category_name
                FROM BOOK b
                LEFT JOIN AUTHOR a ON b.author_id = a.author_id
                LEFT JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
                LEFT JOIN CATEGORY c ON b.category_id = c.category_id
                ORDER BY b.book_id ASC
            """)
            books = cursor.fetchall()
            
            cursor.execute("SELECT * FROM AUTHOR")
            authors = cursor.fetchall()
            
            cursor.execute("SELECT * FROM PUBLISHER")
            publishers = cursor.fetchall()
            
            cursor.execute("SELECT * FROM CATEGORY")
            categories = cursor.fetchall()
            
            return render_template('books.html', books=books, authors=authors, publishers=publishers, categories=categories)
    finally:
        conn.close()

@app.route('/books/add', methods=['POST'])
def add_book():
    book_id = request.form.get('book_id')
    title = request.form.get('title', '').strip()
    price = request.form.get('price')
    publish_year = request.form.get('publish_year') or None
    author_id = request.form.get('author_id')
    publisher_id = request.form.get('publisher_id') or None
    category_id = request.form.get('category_id') or None

    if not book_id or not title or not price or not author_id:
        flash('Book ID, Title, Price, and Author are required.')
        return redirect(url_for('list_books'))

    if int(book_id) < 1 or float(price) < 0:
        flash('IDs and Price cannot be negative.')
        return redirect(url_for('list_books'))

    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            sql = """INSERT INTO BOOK (book_id, title, price, publish_year, author_id, publisher_id, category_id) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (book_id, title, price, publish_year, author_id, publisher_id, category_id))
            conn.commit()
            flash('Book added successfully!')
    except pymysql.MySQLError:
        flash('Error adding book. Check Book ID.')
    finally:
        conn.close()
    return redirect(url_for('list_books'))

@app.route('/books/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM BOOK WHERE book_id = %s", (book_id,))
            conn.commit()
            flash('Deleted book successfully!')
    finally:
        conn.close()
    return redirect(url_for('list_books'))

@app.route('/books/edit/<int:book_id>', methods=['POST'])
def edit_book(book_id):
    title = request.form.get('title', '').strip()
    price = request.form.get('price')
    author_id = request.form.get('author_id')

    if not title or not price or not author_id or float(price) < 0:
        flash('Invalid input or negative price.')
        return redirect(url_for('list_books'))

    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE BOOK SET title = %s, price = %s, author_id = %s WHERE book_id = %s",
                (title, price, author_id, book_id)
            )
            conn.commit()
            flash('Book updated successfully!')
    finally:
        conn.close()
    return redirect(url_for('list_books'))


# ==========================================
# ADD PUBLISHER & CATEGORY ROUTES
# ==========================================

@app.route('/publishers/add', methods=['POST'])
def add_publisher():
    pub_id = request.form.get('publisher_id')
    name = request.form.get('name', '').strip()
    country = request.form.get('country', '').strip()

    if not pub_id or not name or int(pub_id) < 1:
        flash('Valid Publisher ID and Name are required.')
        return redirect(url_for('list_books'))

    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO PUBLISHER (publisher_id, name, country) VALUES (%s, %s, %s)", (pub_id, name, country))
            conn.commit()
            flash('Publisher added successfully!')
    except pymysql.MySQLError:
        flash('Error adding publisher. ID might already exist.')
    finally:
        conn.close()
    return redirect(url_for('list_books'))

@app.route('/categories/add', methods=['POST'])
def add_category():
    cat_id = request.form.get('category_id')
    name = request.form.get('name', '').strip()

    if not cat_id or not name or int(cat_id) < 1:
        flash('Valid Category ID and Name are required.')
        return redirect(url_for('list_books'))

    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO CATEGORY (category_id, name) VALUES (%s, %s)", (cat_id, name))
            conn.commit()
            flash('Category added successfully!')
    except pymysql.MySQLError:
        flash('Error adding category. ID might already exist.')
    finally:
        conn.close()
    return redirect(url_for('list_books'))


# ==========================================
# F2.1: SEARCH BOOKS (WITH PREPARED STATEMENTS BONUS)
# ==========================================

@app.route('/books/search', methods=['GET'])
def search_books():
    keyword = request.args.get('keyword', '').strip()
    min_price = request.args.get('min_price', '').strip()
    max_price = request.args.get('max_price', '').strip()
    category_id = request.args.get('category_id', '').strip()

    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT b.*, a.name AS author_name, p.name AS publisher_name, c.name AS category_name
                FROM BOOK b
                LEFT JOIN AUTHOR a ON b.author_id = a.author_id
                LEFT JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
                LEFT JOIN CATEGORY c ON b.category_id = c.category_id
                WHERE 1=1
            """
            params = []

            if keyword:
                sql += " AND b.title LIKE %s"
                params.append('%' + keyword + '%')
            if min_price:
                sql += " AND b.price >= %s"
                params.append(min_price)
            if max_price:
                sql += " AND b.price <= %s"
                params.append(max_price)
            if category_id:
                sql += " AND b.category_id = %s"
                params.append(category_id)

            sql += " ORDER BY b.price ASC"
            cursor.execute(sql, params)
            books = cursor.fetchall()

            cursor.execute("SELECT * FROM CATEGORY")
            categories = cursor.fetchall()

            return render_template('search_books.html', books=books, categories=categories)
    finally:
        conn.close()


# ==========================================
# F2.3, F2.4, F2.5, F2.6 + MEMBERS & LOANS
# ==========================================

@app.route('/reports')
def reports():
    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM MEMBER ORDER BY member_id ASC")
            all_members = cursor.fetchall()

            cursor.execute("SELECT * FROM BOOK ORDER BY book_id ASC")
            all_books = cursor.fetchall()

            cursor.execute("""
                SELECT l.loan_id, b.title, m.name AS member_name, l.loan_date, l.return_date
                FROM LOAN l
                JOIN BOOK b ON l.book_id = b.book_id
                JOIN MEMBER m ON l.member_id = m.member_id
                ORDER BY l.loan_id DESC
            """)
            all_loans = cursor.fetchall()

            cursor.execute("""
                SELECT c.name AS category_name, COUNT(b.book_id) AS total_books, ROUND(AVG(b.price), 2) AS avg_price
                FROM CATEGORY c
                LEFT JOIN BOOK b ON c.category_id = b.category_id
                GROUP BY c.category_id, c.name
            """)
            cat_stats = cursor.fetchall()

            cursor.execute("""
                SELECT a.name, COUNT(b.book_id) AS book_count
                FROM AUTHOR a
                JOIN BOOK b ON a.author_id = b.author_id
                GROUP BY a.author_id, a.name
                HAVING COUNT(b.book_id) >= 2
            """)
            prolific_authors = cursor.fetchall()

            cursor.execute("SELECT SUM(price) AS total_price, MIN(price) AS min_price, MAX(price) AS max_price FROM BOOK")
            price_summary = cursor.fetchone()

            cursor.execute("""
                SELECT l.loan_id, b.title, m.name AS member_name, l.loan_date
                FROM LOAN l
                JOIN BOOK b ON l.book_id = b.book_id
                JOIN MEMBER m ON l.member_id = m.member_id
                WHERE l.return_date IS NULL
            """)
            active_loans = cursor.fetchall()

            cursor.execute("""
                SELECT m.* FROM MEMBER m
                LEFT JOIN LOAN l ON m.member_id = l.member_id
                WHERE l.loan_id IS NULL
            """)
            inactive_members = cursor.fetchall()

            cursor.execute("""
                SELECT b.* FROM BOOK b
                LEFT JOIN LOAN l ON b.book_id = l.book_id
                WHERE l.loan_id IS NULL
            """)
            unborrowed_books = cursor.fetchall()

            cursor.execute("""
                SELECT b.title, COUNT(l.loan_id) AS loan_count
                FROM BOOK b
                JOIN LOAN l ON b.book_id = l.book_id
                GROUP BY b.book_id, b.title
                ORDER BY loan_count DESC
                LIMIT 3
            """)
            top_books = cursor.fetchall()

            cursor.execute("""
                SELECT m.name, COUNT(l.loan_id) AS loan_count
                FROM MEMBER m
                JOIN LOAN l ON m.member_id = l.member_id
                GROUP BY m.member_id, m.name
                ORDER BY loan_count DESC
                LIMIT 1
            """)
            top_member = cursor.fetchone()

            cursor.execute("""
                SELECT a.name, a.country, COUNT(b.book_id) AS book_count
                FROM AUTHOR a
                LEFT JOIN BOOK b ON a.author_id = b.author_id
                GROUP BY a.author_id, a.name, a.country
            """)
            authors_books_count = cursor.fetchall()

            cursor.execute("""
                SELECT b.title, a.name AS author_name, p.name AS publisher_name, a.country
                FROM BOOK b
                JOIN AUTHOR a ON b.author_id = a.author_id
                JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
                WHERE a.country = p.country
            """)
            same_country_books = cursor.fetchall()

            return render_template(
                'reports.html',
                all_members=all_members,
                all_books=all_books,
                all_loans=all_loans,
                today=date.today().isoformat(),
                cat_stats=cat_stats,
                prolific_authors=prolific_authors,
                price_summary=price_summary,
                active_loans=active_loans,
                inactive_members=inactive_members,
                unborrowed_books=unborrowed_books,
                top_books=top_books,
                top_member=top_member,
                authors_books_count=authors_books_count,
                same_country_books=same_country_books
            )
    finally:
        conn.close()

@app.route('/members/add', methods=['POST'])
def add_member():
    member_id = request.form.get('member_id')
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    join_date = request.form.get('join_date') or date.today().isoformat()

    if not member_id or not name or int(member_id) < 1:
        flash('Valid Member ID and Name are required.')
        return redirect(url_for('reports'))

    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO MEMBER (member_id, name, email, join_date) VALUES (%s, %s, %s, %s)",
                (member_id, name, email, join_date)
            )
            conn.commit()
            flash('Member added successfully!')
    except pymysql.MySQLError:
        flash('Error adding member. Make sure Member ID is unique.')
    finally:
        conn.close()
    return redirect(url_for('reports'))

@app.route('/loans/add', methods=['POST'])
def add_loan():
    loan_id = request.form.get('loan_id')
    book_id = request.form.get('book_id')
    member_id = request.form.get('member_id')
    loan_date = request.form.get('loan_date') or date.today().isoformat()

    if not loan_id or not book_id or not member_id or int(loan_id) < 1:
        flash('Valid Loan ID, Book, and Member are required.')
        return redirect(url_for('reports'))

    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO LOAN (loan_id, book_id, member_id, loan_date, return_date) VALUES (%s, %s, %s, %s, NULL)",
                (loan_id, book_id, member_id, loan_date)
            )
            conn.commit()
            flash('Book borrowed successfully!')
    except pymysql.MySQLError:
        flash('Error adding loan. Make sure Loan ID is unique.')
    finally:
        conn.close()
    return redirect(url_for('reports'))

@app.route('/loans/return/<int:loan_id>', methods=['POST'])
def return_loan(loan_id):
    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE LOAN SET return_date = %s WHERE loan_id = %s",
                (date.today().isoformat(), loan_id)
            )
            conn.commit()
            flash('Book returned successfully!')
    finally:
        conn.close()
    return redirect(url_for('reports'))


# ==========================================
# AUTHORS CRUD ROUTES
# ==========================================

@app.route('/authors/add', methods=['POST'])
def add_author():
    author_id = request.form.get('author_id')
    name = request.form.get('name', '').strip()
    country = request.form.get('country', '').strip()

    if not author_id or not name or not country or int(author_id) < 1:
        flash('Valid Author ID, Name and Country are required.')
        return redirect(url_for('list_books'))

    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO AUTHOR (author_id, name, country) VALUES (%s, %s, %s)", (author_id, name, country))
            conn.commit()
            flash('Author added successfully!')
    except pymysql.MySQLError:
        flash('Error adding author. Make sure Author ID is unique.')
    finally:
        conn.close()
    return redirect(url_for('list_books'))

@app.route('/authors/edit/<int:author_id>', methods=['POST'])
def edit_author(author_id):
    name = request.form.get('name', '').strip()
    country = request.form.get('country', '').strip()

    if not name or not country:
        flash('All fields are required.')
        return redirect(url_for('list_books'))

    form_db = get_library_connection()
    try:
        with form_db.cursor() as cursor:
            cursor.execute("UPDATE AUTHOR SET name = %s, country = %s WHERE author_id = %s", (name, country, author_id))
            form_db.commit()
            flash('Author updated successfully!')
    finally:
        form_db.close()
    return redirect(url_for('list_books'))

@app.route('/authors/delete/<int:author_id>', methods=['POST'])
def delete_author(author_id):
    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM AUTHOR WHERE author_id = %s", (author_id,))
            conn.commit()
            flash('Author and associated books deleted successfully!')
    finally:
        conn.close()
    return redirect(url_for('list_books'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)