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
INSERT INTO student (name, hash)
VALUES (Aidan, pbkdf2:sha256:150000$ts8TeHZ0$c0e79f0fa4a812fc081f7a0a9c5c88b7e9099d6d3b069be237321e9460f7c649);
INSERT INTO student (name, hash)
VALUES (Rob, pbkdf2:sha256:150000$VSoXKJv9$a34e5c53fbdbe525b21c3a85e1bdd48c488b2afbb9feda27634df780eb6d1cb6);
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
    edition    smallint,
    copies     integer
);

# ----
# -- Data dump for book, a total of 5 rows
# ----
INSERT INTO book (isbn,title,author,edition,copies) VALUES ('9780194713535','New Headway C1','Soars, John','5th',2);
INSERT INTO book (isbn,title,author,edition,copies) VALUES ('9780194771818','New Headway B2','Soars, John','5th',1);
INSERT INTO book (isbn,title,author,edition,copies) VALUES ('9781447936879','Cutting Edge B1','Cunningham, Sarah','4th',1);
INSERT INTO book (isbn,title,author,edition,copies) VALUES ('9783125404243','Empower B1','Doff, Adrian','1st',2);
INSERT INTO book (isbn,title,author,edition,copies) VALUES ('9781447936909','Cutting Edge A2-B1','Cunningham, Sarah','5th',3);
# ----
# -- Drop table for transaction
# ----
DROP TABLE IF EXISTS transaction;

# ----
# -- Table structure for transaction
# ----
CREATE TABLE transaction
(
    transaction_type text NOT NULL,
    student_id       varchar(20),
    book_isbn        char(13),
    date             TIMESTAMP DEFAULT (CURRENT_TIMESTAMP)
);

# ----
# -- Data dump for transaction, a total of 7 rows
# ----
INSERT INTO transaction (transaction_type,student_id,book_isbn,date) VALUES ('BORROW','123456789','9780194713535','2021-07-26');
INSERT INTO transaction (transaction_type,student_id,book_isbn,date) VALUES ('BORROW','123456789','9781447936879','2021-08-26');
INSERT INTO transaction (transaction_type,student_id,book_isbn,date) VALUES ('RETURN','123456789','9780194713535','2021-08-27');
INSERT INTO transaction (transaction_type,student_id,book_isbn,date) VALUES ('BORROW','222333444','9781447936879','2021-07-26');
INSERT INTO transaction (transaction_type,student_id,book_isbn,date) VALUES ('BORROW','222333444','9780194713535','2021-07-26');
INSERT INTO transaction (transaction_type,student_id,book_isbn,date) VALUES ('RETURN','123456789','9781447936879','2021-07-26');
INSERT INTO transaction (transaction_type,student_id,book_isbn,date) VALUES ('RETURN','222333444','9780194713535','2021-07-26');
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

