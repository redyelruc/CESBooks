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
    edition    varchar(10),
    copies     integer
);

# ----
# -- Data dump for book, a total of 5 rows
# ----
INSERT INTO book (isbn,title,author,edition,copies) VALUES ("9780194713535","New Headway C1","Soars, John","5th","2");
INSERT INTO book (isbn,title,author,edition,copies) VALUES ("9780194771818","New Headway B2","Soars, John","5th","1");
INSERT INTO book (isbn,title,author,edition,copies) VALUES ("9781447936879","Cutting Edge B1","Cunningham, Sarah","4th","1");
INSERT INTO book (isbn,title,author,edition,copies) VALUES ("9783125404243","Empower B1","Doff, Adrian","1st","2");
INSERT INTO book (isbn,title,author,edition,copies) VALUES ("9781447936909","Cutting Edge A2-B1","Cunningham, Sarah","5th","3");
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
    date_borrowed    TIMESTAMP DEFAULT (CURRENT_TIMESTAMP),
    date_returned    TIMESTAMP
);

# ----
# -- Data dump for transaction, a total of 7 rows
# ----
INSERT INTO transaction (student_id,book_isbn,date_borrowed, date_returned) VALUES ("123456789","9780194713535","2021-11-26","2021-11-29");
INSERT INTO transaction (student_id,book_isbn,date_borrowed, date_returned) VALUES ("123456789","9781447936879","2021-11-26","2021-11-30");
INSERT INTO transaction (student_id,book_isbn,date_borrowed, date_returned) VALUES ("123123123","9780194713535","2021-11-27","2021-12-05");
INSERT INTO transaction (student_id,book_isbn,date_borrowed, date_returned) VALUES ("222333444","9781447936879","2021-11-26","2021-12-05");
INSERT INTO transaction (student_id,book_isbn,date_borrowed) VALUES ("222333444","9780194713535","2021-12-06");
INSERT INTO transaction (student_id,book_isbn,date_borrowed) VALUES ("123456789","9781447936879","2021-12-01");
INSERT INTO transaction (student_id,book_isbn,date_borrowed) VALUES ("123123123","9780194713535","2021-12-04");
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

