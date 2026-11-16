DROP DATABASE IF EXISTS company;
CREATE DATABASE company;
USE company;
CREATE TABLE EMPLOYEE (
    ssn INT NOT NULL,
    fname VARCHAR(30) NOT NULL,
    lname VARCHAR(30) NOT NULL,
    bdate DATE,
    address VARCHAR(100),
    gender VARCHAR(10),
    salary DECIMAL(10,2),
    super_ssn INT,
    Dno INT,
    PRIMARY KEY (ssn),
    FOREIGN KEY (super_ssn) REFERENCES EMPLOYEE(ssn) ON DELETE SET NULL
);

CREATE TABLE DEPARTMENT (
    Dnumber INT NOT NULL,
    Dname VARCHAR(50) NOT NULL,
    mgr_ssn INT,
    mgr_start_date DATE,
    PRIMARY KEY (Dnumber),
    FOREIGN KEY (mgr_ssn) REFERENCES EMPLOYEE(ssn) ON DELETE SET NULL
);

ALTER TABLE EMPLOYEE ADD CONSTRAINT fk_emp_dept FOREIGN KEY (Dno) REFERENCES DEPARTMENT(Dnumber);

CREATE TABLE PROJECT (
    Pnumber INT NOT NULL,
    Pname VARCHAR(50) NOT NULL,
    Plocation VARCHAR(50),
    Dno INT,
    PRIMARY KEY (Pnumber),
    FOREIGN KEY (Dno) REFERENCES DEPARTMENT(Dnumber)
);
CREATE TABLE WORKS_ON (
    essn INT NOT NULL,
    Pno INT NOT NULL,
    hours DECIMAL(4,1),
    PRIMARY KEY (essn, Pno),
    FOREIGN KEY (essn) REFERENCES EMPLOYEE(ssn) ON DELETE CASCADE,
    FOREIGN KEY (Pno) REFERENCES PROJECT(Pnumber) ON DELETE CASCADE
);
CREATE TABLE DEPENDENT (
    essn INT NOT NULL,
    dependent_name VARCHAR(30) NOT NULL,
    gender VARCHAR(10),
    bdate DATE,
    relationship VARCHAR(20),
    PRIMARY KEY (essn, dependent_name),
    FOREIGN KEY (essn) REFERENCES EMPLOYEE(ssn) ON DELETE CASCADE
);