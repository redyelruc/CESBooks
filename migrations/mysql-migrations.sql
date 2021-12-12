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
    name     varchar(30) NOT NULL,
    hash     text NOT NULL
);

# ----
# -- Data dump for student, a total of 2 rows
# ----
INSERT INTO student (id, name, hash)
VALUES ("123456789", "Aidan", "pbkdf2:sha256:150000$ts8TeHZ0$c0e79f0fa4a812fc081f7a0a9c5c88b7e9099d6d3b069be237321e9460f7c649");
INSERT INTO student (id, name, hash)
VALUES ("222333444", "Rob", "pbkdf2:sha256:150000$VSoXKJv9$a34e5c53fbdbe525b21c3a85e1bdd48c488b2afbb9feda27634df780eb6d1cb6");
# ----
# -- Drop table for book
# ----
DROP TABLE IF EXISTS book;

# ----
# -- Table structure for book
# ----
CREATE TABLE book
(
    isbn       varchar(13) NOT NULL,
    title      varchar(100),
    author     varchar(100),
    year    varchar(10),
    copies     integer
);

# ----
# -- Data dump for book, a total of 7 rows
# ----
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9781491952023","JavaScript: The Definitive Guide","David Flanagan","2020","2");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9781937785499","Programming Ruby 1.9 & 2.0 - The Pragmatic Programmers\' Guide","David Thomas","2013","2");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9780135957059","The Pragmatic Programmer","David Thomas","2019","1");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9780596516178","The Ruby Programming Language","David Flanagan","2008","1");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9780132350884","Clean Code - A Handbook Of Agile Software Craftsmanship ","Robert C, Martin","2009","1");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9781593279288","Python Crash Course, 2nd Edition - A Hands-On, Project-Based Introduction To Programming","Eric Mathes","2019","1");
INSERT INTO book (isbn,title,author,year,copies) VALUES ("9781449369415","Introduction To Machine Learning With Python - A Guide For Data Scientists","Andreas C. Müller","2016","2");

# ----
# -- Drop table for transaction
# ----
DROP TABLE IF EXISTS transaction;

# ----
# -- Table structure for transaction
# ----
CREATE TABLE transaction
(
    student_id       varchar(20),
    book_isbn        char(13),
    date_borrowed    DATE,
    date_returned    DATE
);

# ----
# -- Data dump for transaction, a total of 5 rows
# ----
INSERT INTO transaction (student_id,book_isbn,date_borrowed, date_returned) VALUES ("123456789","9780596516178","2021-11-21","2021-11-29");
INSERT INTO transaction (student_id,book_isbn,date_borrowed, date_returned) VALUES ("123456789","9781937785499","2021-11-26","2021-11-30");
INSERT INTO transaction (student_id,book_isbn,date_borrowed, date_returned) VALUES ("123456789","9780132350884","2021-11-27","2021-12-05");
INSERT INTO transaction (student_id,book_isbn,date_borrowed, date_returned) VALUES ("222333444","9781491952023","2021-11-20","2021-12-05");
INSERT INTO transaction (student_id,book_isbn,date_borrowed, date_returned) VALUES ("222333444","9780132350884","2021-12-01","0000-00-00");
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

