USE company;
INSERT INTO DEPARTMENT (Dnumber, Dname, mgr_ssn, mgr_start_date) VALUES 
(1, 'Research', NULL, '2020-01-01'),
(2, 'Administration', NULL, '2019-05-15'),
(3, 'Development', NULL, '2021-03-10'),
(4, 'EmptyDept', NULL, '2023-01-01');

INSERT INTO EMPLOYEE (ssn, fname, lname, bdate, address, gender, salary, super_ssn, Dno) VALUES 
(101, 'Salma', 'Khaled', '2004-05-12', 'Alexandria', 'Female', 6500.00, NULL, 1),
(102, 'Ahmed', 'Ali', '2000-02-10', 'Cairo', 'Male', 4500.00, 101, 1),
(103, 'Mohamed', 'Hassan', '1998-07-22', 'Giza', 'Male', 2800.00, 101, 2),
(104, 'Mona', 'Ibrahim', '2001-11-05', 'Alexandria', 'Female', 5200.00, 102, 2),
(105, 'Omar', 'Khaled', '1995-12-30', 'Aswan', 'Male', 3100.00, NULL, 3),
(106, 'Fatma', 'Zohairy', '1999-09-19', 'Alexandria', 'Female', 7000.00, 101, 3);

UPDATE DEPARTMENT SET mgr_ssn = 101 WHERE Dnumber = 1;
UPDATE DEPARTMENT SET mgr_ssn = 103 WHERE Dnumber = 2;
UPDATE DEPARTMENT SET mgr_ssn = 106 WHERE Dnumber = 3;

INSERT INTO PROJECT (Pnumber, Pname, Plocation, Dno) VALUES 
(10, 'Alpha', 'Alexandria', 1),
(20, 'Beta', 'Cairo', 2),
(30, 'Gamma', 'Aswan', 3),
(40, 'UnassignedProject', 'Luxor', 1);
INSERT INTO WORKS_ON (essn, Pno, hours) VALUES 
(101, 10, 15.0),
(101, 20, 10.0), 
(102, 10, 5.0),
(103, 20, 12.0),
(104, 20, 8.0),
(105, 30, 22.0),
(106, 30, 5.0),
(102, 20, 6.0);

INSERT INTO DEPENDENT (essn, dependent_name, gender, bdate, relationship) VALUES 
(101, 'Zain', 'Male', '2022-01-01', 'Son'),
(102, 'Laila', 'Female', '2023-05-10', 'Daughter'),
(103, 'Sara', 'Female', '2020-08-15', 'Wife');