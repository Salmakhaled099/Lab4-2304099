DROP DATABASE IF EXISTS library;
CREATE DATABASE library;
USE library;

CREATE TABLE AUTHOR (
    author_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    country VARCHAR(30),
    PRIMARY KEY (author_id)
);

CREATE TABLE PUBLISHER (
    publisher_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    country VARCHAR(30),
    PRIMARY KEY (publisher_id)
);

CREATE TABLE CATEGORY (
    category_id INT NOT NULL,
    name VARCHAR(30) NOT NULL,
    PRIMARY KEY (category_id)
);

CREATE TABLE BOOK (
    book_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    price DECIMAL(10,2),
    publish_year INT,
    author_id INT,
    publisher_id INT,
    category_id INT,
    PRIMARY KEY (book_id),
    FOREIGN KEY (author_id) REFERENCES AUTHOR(author_id) ON DELETE CASCADE,
    FOREIGN KEY (publisher_id) REFERENCES PUBLISHER(publisher_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES CATEGORY(category_id) ON DELETE CASCADE
);

CREATE TABLE MEMBER (
    member_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50),
    join_date DATE,
    PRIMARY KEY (member_id)
);

CREATE TABLE LOAN (
    loan_id INT NOT NULL,
    book_id INT,
    member_id INT,
    loan_date DATE,
    return_date DATE,
    PRIMARY KEY (loan_id),
    FOREIGN KEY (book_id) REFERENCES BOOK(book_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES MEMBER(member_id) ON DELETE CASCADE
);