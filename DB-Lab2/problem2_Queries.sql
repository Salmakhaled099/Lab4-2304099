USE library;

-- F2.1 Search books (WHERE, LIKE, BETWEEN)
-- SELECT * FROM book WHERE title LIKE '%keyword%' AND price BETWEEN min_price AND max_price AND category_id = cat_id ORDER BY price ASC;

-- F2.2 Catalogue (JOIN)
SELECT b.title, b.price, a.name AS author_name, p.name AS publisher_name, c.name AS category_name
FROM BOOK b
JOIN AUTHOR a ON b.author_id = a.author_id
JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
JOIN CATEGORY c ON b.category_id = c.category_id;

-- F2.3 Reports (GROUP BY, HAVING, Aggregate)
-- (a) Number of books and average price per category
SELECT c.name AS category_name, COUNT(b.book_id) AS total_books, AVG(b.price) AS avg_price
FROM CATEGORY c
LEFT JOIN BOOK b ON c.category_id = b.category_id
GROUP BY c.category_id, c.name;

-- (b) Authors who wrote at least 2 books
SELECT a.name, COUNT(b.book_id) AS book_count
FROM AUTHOR a
JOIN BOOK b ON a.author_id = b.author_id
GROUP BY a.author_id, a.name
HAVING COUNT(b.book_id) >= 2;

-- (c) Total, smallest and largest price of the whole library
SELECT SUM(price) AS total_price, MIN(price) AS min_price, MAX(price) AS max_price FROM BOOK;

-- F2.4 Loans (JOIN, LEFT JOIN)
-- (a) Loans not returned yet
SELECT l.loan_id, b.title, m.name AS member_name, l.loan_date
FROM LOAN l
JOIN BOOK b ON l.book_id = b.book_id
JOIN MEMBER m ON l.member_id = m.member_id
WHERE l.return_date IS NULL;

-- (b) Members who never borrowed a book
SELECT m.* FROM MEMBER m
LEFT JOIN LOAN l ON m.member_id = l.member_id
WHERE l.loan_id IS NULL;

-- (c) Books that were never borrowed
SELECT b.* FROM BOOK b
LEFT JOIN LOAN l ON b.book_id = l.book_id
WHERE l.loan_id IS NULL;

-- F2.5 Most borrowed (GROUP BY, ORDER BY, LIMIT)
-- Top 3 books with most loans
SELECT b.title, COUNT(l.loan_id) AS loan_count
FROM BOOK b
JOIN LOAN l ON b.book_id = l.book_id
GROUP BY b.book_id, b.title
ORDER BY loan_count DESC
LIMIT 3;

-- Member with most loans
SELECT m.name, COUNT(l.loan_id) AS loan_count
FROM MEMBER m
JOIN LOAN l ON m.member_id = l.member_id
GROUP BY m.member_id, m.name
ORDER BY loan_count DESC
LIMIT 1;

-- F2.6 Authors and books
-- (a) Every author with number of books (including 0)
SELECT a.name, COUNT(b.book_id) AS book_count
FROM AUTHOR a
LEFT JOIN BOOK b ON a.author_id = b.author_id
GROUP BY a.author_id, a.name;

-- (b) Books whose author and publisher come from the same country
SELECT b.title, a.name AS author_name, p.name AS publisher_name, a.country
FROM BOOK b
JOIN AUTHOR a ON b.author_id = a.author_id
JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
WHERE a.country = p.country;