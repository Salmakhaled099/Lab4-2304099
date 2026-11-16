USE library;

INSERT INTO AUTHOR VALUES 
(1, 'Naguib Mahfouz', 'Egypt'),
(2, 'Taha Hussein', 'Egypt'),
(3, 'Agatha Christie', 'UK'),
(4, 'Dan Brown', 'USA'),
(5, 'Author With No Books', 'Egypt');

INSERT INTO PUBLISHER VALUES 
(1, 'Dar El Shorouk', 'Egypt'),
(2, 'Penguin Books', 'UK'),
(3, 'Doubleday', 'USA');

INSERT INTO CATEGORY VALUES 
(1, 'Fiction'),
(2, 'Mystery'),
(3, 'History');

INSERT INTO BOOK VALUES 
(101, 'Palace Walk', 18.50, 1956, 1, 1, 1), 
(102, 'Sugar Street', 22.00, 1957, 1, 1, 1),
(103, 'The Days', 14.00, 1929, 2, 1, 3),
(104, 'And Then There Were None', 16.00, 1939, 3, 2, 2),
(105, 'The Da Vinci Code', 25.00, 2003, 4, 3, 1),
(106, 'Never Borrowed Book', 19.99, 2020, 2, 1, 1),
(107, 'Miramar', 17.50, 1967, 1, 1, 1),
(108, 'Murder on the Orient Express', 21.00, 1934, 3, 2, 2),
(109, 'Angels & Demons', 24.00, 2000, 4, 3, 2),
(110, 'The Future of Culture in Egypt', 15.00, 1938, 2, 1, 3);

INSERT INTO MEMBER VALUES 
(1, 'Salma Khaled', 'salma@email.com', '2025-01-01'),
(2, 'Ahmed Ali', 'ahmed@email.com', '2025-02-01'),
(3, 'Mona Mohamed', 'mona@email.com', '2025-03-01'),
(4, 'Omar Youssef', 'omar@email.com', '2025-04-01'),
(5, 'No Loans Member', 'noloans@email.com', '2025-05-01'); 

INSERT INTO LOAN VALUES 
(1, 101, 1, '2026-01-10', '2026-01-20'),
(2, 102, 1, '2026-02-01', '2026-02-15'),
(3, 103, 2, '2026-03-01', '2026-03-10'),
(4, 104, 3, '2026-03-05', NULL),
(5, 105, 4, '2026-03-11', '2026-03-15'),
(6, 101, 2, '2026-03-12', '2026-03-20'),
(7, 102, 3, '2026-03-15', '2026-03-25'),
(8, 103, 4, '2026-03-18', '2026-03-22'),
(9, 104, 1, '2026-03-20', '2026-03-28'),
(10, 105, 2, '2026-03-22', '2026-03-30'),
(11, 101, 3, '2026-03-25', '2026-04-02'),
(12, 103, 1, '2026-04-01', '2026-04-05');