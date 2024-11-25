-- Create the schema (database) if it doesn't already exist
CREATE SCHEMA IF NOT EXISTS assignment_3;

-- Use the schema (database)
USE assignment_3;

CREATE TABLE Student (
    student_id INT PRIMARY KEY,
    name VARCHAR(255),
    age INT
);

CREATE TABLE Course (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(255),
    credits INT
);

CREATE TABLE Enrollment (
    student_id INT,
    course_id INT,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

CREATE TABLE Book (
    book_id INT PRIMARY KEY,
    title VARCHAR(255),
    publication_year INT
);

CREATE TABLE Author (
    author_id INT PRIMARY KEY,
    name VARCHAR(255),
    nationality VARCHAR(255)
);

CREATE TABLE Book_Author (
    book_id INT,
    author_id INT,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES Book(book_id),
    FOREIGN KEY (author_id) REFERENCES Author(author_id)
);

CREATE TABLE Project (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(255),
    deadline DATE
);

CREATE TABLE Employee (
    employee_id INT PRIMARY KEY,
    name VARCHAR(255),
    position VARCHAR(255)
);

CREATE TABLE Project_Employee (
    project_id INT,
    employee_id INT,
    PRIMARY KEY (project_id, employee_id),
    FOREIGN KEY (project_id) REFERENCES Project(project_id),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
);
