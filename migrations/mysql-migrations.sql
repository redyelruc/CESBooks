#CREATE {DATABASE | SCHEMA} [IF NOT EXISTS] finance;
USE finance;
# ----
# -- Drop table for student
# ----
DROP TABLE IF EXISTS student;

# ----
# -- Table structure for student
# ----
CREATE TABLE student
(
    id       varchar(20) PRIMARY KEY NOT NULL,
    hash     text NOT NULL
);

# ----
# -- Data dump for student, a total of 2 rows
# ----
INSERT INTO student (id, hash)
VALUES ("c7465688", "pbkdf2:sha256:150000$VSoXKJv9$a34e5c53fbdbe525b21c3a85e1bdd48c488b2afbb9feda27634df780eb6d1cb6"),
       ("c1231231", "pbkdf2:sha256:260000$Istb2ASlVkANwJ7d$70d3a1b382fa60476058a7298322d0b6a6f09415518cca288d40c6311b406e6f");

# ----
# -- Drop table for book
# ----
DROP TABLE IF EXISTS book;

# ----a
# -- Table structure for book
# ----
CREATE TABLE book
(
    isbn       varchar(13) NOT NULL,
    title      varchar(100),
    author     varchar(100),
    year       integer,
    copies     integer
);

# ----
# -- Data dump for book, a total of 7 rows
# ----
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9781491952023", "JavaScript: The Definitive Guide", "David Flanagan", "2020", "2");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9781937785499", "Programming Ruby 1.9 & 2.0 - The Pragmatic Programmers\' Guide", "David Thomas", "2013", "2");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9780135957059", "The Pragmatic Programmer", "David Thomas", "2019", "1");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9780596516178", "The Ruby Programming Language", "David Flanagan", "2008", "1");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9780132350884", "Clean Code - A Handbook Of Agile Software Craftsmanship", "Robert C. Martin", "2009", "1");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9781593279288", "Python Crash Course, 2nd Edition - A Hands-On, Project-Based Introduction To Programming", "Eric Mathes", "2019", "1");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9781449369415", "Introduction To Machine Learning With Python - A Guide For Data Scientists", "Andreas C. Muller", "2016", "2");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9781617298691", "Spring Start Here - Learn What You Need And Learn It Well", "Laurentiu Spilca", "2021", "2");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9781430265337", "Introducing Spring Framework - A Primer","Felipe Gutierrez", "2014", "1");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9781491956250", "Microservice Architecture - Aligning Principles, Practices, And Culture", "Irakli Nadareishvili", "2016", "2");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9783319994192", "Java in two semesters (4th edition)", "Quentin Charatan", "2019", "1");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9780321349606", "Java concurrency in practice","Brian Goetz", "2015", "2");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9781543057386", "Distributed systems (3rd edition)","Maarten van Steen", "2017", "2");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9781292097619", "Fundamentals of database systems (7th edition)", "Ramez Elmasri", "2016", "2");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9789813221871", "An Introduction To Component-Based Software Development", "Lau Kung-Kiu", "2017", "1");
# ----
# -- Drop table for transaction
# ----
DROP TABLE IF EXISTS transaction;

# ----
# -- Table structure for transaction
# ----
CREATE TABLE transaction
(
    id               integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    student_id       varchar(20),
    book_isbn        char(13),
    date_borrowed    DATE,
    date_returned    DATE
);

# ----
# -- Data dump for transaction, a total of 5 rows
# ----
INSERT INTO transaction (student_id,book_isbn,date_borrowed, date_returned) VALUES ("c7465688","9780596516178","2021-11-21","2021-11-29");
INSERT INTO transaction (student_id,book_isbn,date_borrowed, date_returned) VALUES ("c7465688","9781937785499","2021-11-26","2021-11-30");
INSERT INTO transaction (student_id,book_isbn,date_borrowed, date_returned) VALUES ("c7465688","9780132350884","2021-11-27","2021-12-05");
INSERT INTO transaction (student_id,book_isbn,date_borrowed, date_returned) VALUES ("c7465688","9781491952023","2021-11-20","2021-12-05");
INSERT INTO transaction (student_id,book_isbn,date_borrowed, date_returned) VALUES ("c7465688","9781937785499","2021-11-23","0000-00-00");
INSERT INTO transaction (student_id,book_isbn,date_borrowed, date_returned) VALUES ("c7465688","9780132350884","2021-11-01","0000-00-00");
# ----
# -- structure for index name on table student
# ----
ALTER TABLE student
    ADD UNIQUE (id(20));
COMMIT;

# ----
# -- make isbn primary key
# ----
ALTER TABLE book
ADD PRIMARY KEY(isbn);
COMMIT;

