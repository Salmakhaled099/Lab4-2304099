# DB Lab 4 - Search Queries in SQL & Library Management System

## Team Members
* Salma Khaled - ID: 2304099

## Tech Stack
* **Back-end:** Python (Flask), PyMySQL, bcrypt, python-dotenv
* **Front-end:** HTML5, CSS3, Bootstrap 5
* **Database:** MySQL

---

## Project Structure

text
lab4-2304099/
├── problem1_DDL.sql        # Schema creation for Company database (5 tables)
├── problem1_DML.sql        # Seed data for Company database
├── problem1_Answers.txt    # SQL queries and outputs/errors for Q1.1 - Q1.12
├── problem2_DDL.sql        # Schema creation for Library database (6 tables with ON DELETE CASCADE)
├── problem2_DML.sql        # Seed data for Library database (Authors, Publishers, Categories, Books, Members, Loans)
├── problem2_Queries.sql    # SQL queries for website features F2.1 - F2.6
├── website/                # Flask web application extending Lab 3
│   ├── app.py
│   ├── schema.sql
│   ├── .env.example
│   ├── templates/
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── books.html
│   │   ├── search_books.html
│   │   └── reports.html
│   └── static/
└── README.md

Step-by-Step Setup & How to Run
1. Database Setup (MySQL)
Run the SQL scripts using the MySQL client (or DBeaver) in the exact order below:
# Part I: Company Database
mysql -u root -p < problem1_DDL.sql
mysql -u root -p < problem1_DML.sql

# Part II: Library Database
mysql -u root -p < problem2_DDL.sql
mysql -u root -p < problem2_DML.sql

# Authentication / To-Do Database (from Lab 3)
mysql -u root -p < website/schema.sql

2. Website Setup (Flask)
 * Navigate to the website/ folder:
   cd website

 * Install the required Python dependencies:
   pip install flask pymysql bcrypt python-dotenv

 * Configure environment variables:
   * Copy .env.example to .env and set your DB_HOST, DB_USER, DB_PASSWORD, and SECRET_KEY.
 * Start the Flask server:
   python app.py

 * Open your browser and navigate to:
   * Login / To-Do App: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
   * Library Catalogue & Management (F2.2): [http://127.0.0.1:5000/books](http://127.0.0.1:5000/books)
   * Search Books with Prepared Statements Bonus (F2.1): [http://127.0.0.1:5000/books/search](http://127.0.0.1:5000/books/search)
   * Reports, Members, Loans & Analytics (F2.3 - F2.6): [http://127.0.0.1:5000/reports](http://127.0.0.1:5000/reports)
Features & Deliverables
 * Problem 1 (company database):
   * Extended 5-table schema (EMPLOYEE, DEPARTMENT, PROJECT, WORKS_ON, DEPENDENT) with self-referencing and composite keys.
   * Complete SQL queries and outputs/error explanations for Q1.1 through Q1.12 in problem1_Answers.txt.
 * Problem 2 (library database & Website):
   * 6-table relational schema (AUTHOR, PUBLISHER, CATEGORY, BOOK, MEMBER, LOAN) with ON DELETE CASCADE.
   * F2.1 Search Books: Filter books by title keyword (LIKE), price range (BETWEEN), and category, sorted cheapest first.
   * F2.2 Catalogue: Displays full book details joined with Author, Publisher, and Category names, plus full CRUD management for Authors, Publishers, Categories, and Books with input validation.
   * F2.3 Reports: Category book counts & average prices, authors with 2+ books (GROUP BY / HAVING), and overall library price summary (SUM, MIN, MAX).
   * F2.4 Loans: Active unreturned loans, members who never borrowed a book, unborrowed books, plus interactive Member registration and Book Borrow/Return actions.
   * F2.5 Most Borrowed: Top 3 most borrowed books and the most active library member.
   * F2.6 Authors & Books: Book counts for all authors (including 0 via LEFT JOIN) and books where author and publisher share the same country.
   * Bonus: Parameterized queries (Prepared Statements) used in /books/search to prevent SQL Injection.
