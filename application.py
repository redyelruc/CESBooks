from datetime import date

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp

from book import Book
from constants import MAX_BORROWING_DURATION, INVOICES_URL
from errors import IncompleteBookError
from fine import Fine

from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, calculate_days_overdue, days_before
import isbnlib
import requests

# Configure application
from transaction import Transaction

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    db.execute("COMMIT;")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQL database
db = SQL("mysql://redyelruc:financered180974finance@127.0.0.1:3306/finance")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if not request.form.get("student_id"):
            return apology("must provide student_id", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM student WHERE id = %s", request.form.get("student_id"))
        # Ensure student_id exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid details", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# @login_required
# @app.route("firstlogin")
# def firstlogin():
#     """Update Password"""


@app.route("/register", methods=["POST"])
def register():
    """Register user"""
    student_id = request.json['student_id']
    # check student_id is not already registered
    if db.execute("SELECT * FROM student WHERE id = %s", student_id):
        return student_id, 204

    # create row in db with default password
    db.execute("INSERT INTO student(id, hash) VALUES (%s, %s)", student_id, generate_password_hash("000000"))
    return student_id, 201


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/", methods=["GET"])
@login_required
def books():
    """List all books"""
    rows = db.execute("SELECT * FROM book ORDER BY title")
    booklist = []

    for row in rows:
        booklist.append([row['isbn'], row['title'], row['author'], row['year'], row['copies']])

    if request.method == "GET":
        return render_template("books.html", books=booklist)


@app.route("/history")
@login_required
def transactions():
    """Show history of transactions"""
    rows = db.execute(
        "SELECT * FROM transaction WHERE student_id = %s ORDER BY date_returned ASC, date_borrowed DESC LIMIT 8",
        session["user_id"])
    transaction_history = []
    for row in rows:
        transaction_history.append([row['date_borrowed'], row['date_returned'], row['book_isbn'],
                                    calculate_days_overdue(row['date_borrowed'], row['date_returned'])])

    # redirect user to index page
    return render_template("transactions.html", transactions=transaction_history)


@app.route("/borrow", methods=["GET", "POST"])
@login_required
def borrow():
    """Borrow a book"""
    if request.method == "GET":
        return render_template("borrow.html", books=books)
    else:
        isbn = request.form.get("isbn")
        today = date.today().strftime('%Y-%m-%d')
        copies_available = int(db.execute("SELECT copies from book WHERE isbn = %s", isbn)[0]['copies'])

        if not copies_available:
            return apology('Sorry, no copies available')
        else:
            db.execute("UPDATE book SET copies = copies -1 WHERE isbn = %s", isbn)
            db.execute("INSERT INTO transaction VALUES (%s, %s, %s, %s)", session["user_id"], isbn, today, '0000:00:00')

        flash("Book has been borrowed.")
        return redirect("/history")


@app.route("/return_books", methods=["GET", "POST"])
@login_required
def return_books():
    """Return a book"""
    if request.method == "GET":
        return render_template("return.html")
    else:
        today = date.today().strftime('%Y-%m-%d')
        book = select_book(request.form.get("isbn"))

        if not book:
            flash("This book is not in our database.")
            return redirect("/books")

        # RETURN A BOOK
        try:
            records = db.execute(
                "SELECT * FROM transaction WHERE book_isbn = %s AND student_id = %s AND date_returned = '0000:00:00'",
                book.isbn, session["user_id"])

            if len(records) != 1:
                flash("This is not one of the books you have borrowed.")
                return redirect("/history")

            transaction = Transaction(records[0])

            db.execute("UPDATE transaction SET date_returned = %s WHERE id = %s", today, transaction.id)
            db.execute("UPDATE book SET copies = copies + 1 WHERE isbn = %s", book.isbn)
            message = 'Thanks for your return.'

            # check, and issue fine if needed
            if days_before(transaction.date_borrowed, date.today()) > MAX_BORROWING_DURATION:
                fine = Fine(transaction.date_borrowed, session["user_id"])
                r = requests.post(INVOICES_URL, json=fine.details)

                message += f" You have been fined £{fine.amount}. Please log in to the Payment Portal to pay the " \
                           f"invoice reference: {r.json()['reference']}. "
            flash(message)
        except Exception as e:
            print(e)

    return redirect("/history")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add a new title to the library."""
    if request.method == "GET":
        return render_template("add.html")
    else:
        isbn = request.form.get("isbn")
        details = isbnlib.meta(isbn)
        cover = isbnlib.cover(isbn)
        book_details = {'isbn': details['ISBN-13'], 'title': details['Title'], 'author': details['Authors'][0],
                        'year': details['Year'], 'cover': cover['thumbnail'], 'copies': 1}
        return render_template("addstock.html", **book_details)


@app.route("/addstock", methods=["POST"])
@login_required
def addstock():
    try:
        book = Book(request.form.get("isbn"), request.form.get("title"), request.form.get("author"),
                    request.form.get("year"), request.form.get("copies"))
        db.execute("INSERT INTO book(isbn, title, author, year, copies) VALUES(%s, %s, %s, %s, %s)",
                   book.isbn, book.title, book.author, book.year, book.copies)

        flash(f"{book.title} added")
        return redirect("/")
    except (IncompleteBookError, ValueError) as e:
        flash(f'{e} The book was not added to the database.')
        return render_template("add.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


def select_book(isbn):
    book_records = db.execute("SELECT * FROM book WHERE isbn = %s", isbn)
    return None if not book_records else Book(book_records[0])


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
