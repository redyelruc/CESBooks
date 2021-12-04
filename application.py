import os
from datetime import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
import isbnlib


# Configure application
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

# Configure CS50 Library to use SQLite database
#'mysql://<your_student_id>:<your_mysql_password>@<your_mysql_hostname>/<your_database_name>'
db = SQL(os.environ['DATABASE'])

@app.route("/")
@login_required
def index():
    """Show all books"""

    rows = db.execute("SELECT * FROM book ORDER BY title")
    books =[]
    for row in rows:
        books.append([row['isbn'], row['title'], row['author'], row['edition'], row['copies']])
    return render_template("index.html", books=books)


@app.route("/transactions")
@login_required
def transactions():
    """Show history of transactions"""
    rows = db.execute("SELECT * FROM transaction WHERE DATE(date) = CURDATE() ORDER BY date DESC")
    transaction_history =[]
    for row in rows:
        transaction_history.append([row['date'], row['transaction_type'], row['book_isbn'], row['student_id']])

    # redirect user to index page
    return render_template("transactions.html", transactions=transaction_history)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure student_id was submitted
        if not request.form.get("student_id"):
            return apology("must provide student_id", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for student_id
        rows = db.execute("SELECT * FROM student WHERE id = :student_id",
                          student_id=request.form.get("student_id"))

        # Ensure student_id exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid details", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        # Display form for user to create account
        return render_template("register.html")
    else:
        # register the new user
        # check student_id is not blank
        if not request.form.get("student_id"):
            return apology("must provide student_id", 403)
        # check password id not blank
        if not request.form.get("password"):
            return apology('must provide password', 403)
        # check student_id is unique
        if db.execute("SELECT * FROM student WHERE id = :student_id", student_id=request.form.get("student_id")):
            return apology("you already have an account", 403)
        # check password and confirmation are same
        if request.form.get("password") != request.form.get("confirm-password"):
            return apology("password and confirmation do not match", 403)
        # hash the password and create row in db
        db.execute("INSERT INTO student(id, hash) VALUES (:student_id, :hash)", student_id=request.form.get("student_id"),
                   hash=generate_password_hash(request.form.get("password")))

        # make sure that the new user is logged in
        rows = db.execute("SELECT * FROM student WHERE id = :student_id", student_id=request.form.get("student_id"))
        # set the session so we know who is logged in
        session["user_id"] = rows[0]["id"]
        return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Loan a book"""
    rows = db.execute("SELECT * FROM book ORDER BY title")
    books =[]
    transaction = "BORROW"
    for row in rows:
        books.append([row['isbn'], row['title'], row['author'], row['edition'], row['copies']])
    if request.method == "GET":
        return render_template("borrow.html", books=books)
    else:
        isbn = request.form.get("isbn")
        student_id = request.form.get("student_id")
        # check database to make sure book is available
        copies_available = db.execute("SELECT copies from book WHERE isbn = :isbn", isbn = isbn)

        if not copies_available:
            return apology('Sorry, no copies available')
        else:
            db.execute("UPDATE book SET copies = :books_left WHERE isbn = :isbn", isbn = isbn,
                    books_left = int(copies_available[0]) - 1)
            db.execute("INSERT INTO transaction(transaction_type, student_id, book_isbn, date) VALUES (:trans, :student, :isbn, :date)",
                        trans=transaction, student=session["user_id"], isbn=isbn, date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        flash("Book has been loaned!")
        return redirect("/")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Return a book"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        isbn = request.form.get("isbn")
        student = request.form.get("student_id")
        transaction = "RETURN"
        # get current stock level
        copies_available = db.execute("SELECT * from book WHERE isbn = :isbn", isbn = isbn)
        try:
            # add one to stock level and write to database
            db.execute("UPDATE books SET copies = :copies WHERE isbn = :isbn", isbn = isbn, copiess = copies_available[0] + 1)
            # record in transactions database
            db.execute("INSERT INTO transaction(transaction_type, student_id, book_isbn, date) VALUES (:trans, :student, :isbn, :date)",
                            trans=transaction, student=session["user_id"], isbn=isbn, date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            flash("Book has been returned!")
            return redirect("/")
        except IndexError:
            apology("Not in database.")
            return


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Get stock quote."""
    if request.method == "GET":
        # Display form for user to enter stock to search
        return render_template("add.html")
    else:
        isbn = request.form.get("isbn")
        book_details = isbnlib.meta(isbn)
        cover = isbnlib.cover(isbn)
        book_details['cover']=cover['thumbnail']
        if "ISBN-13" in book_details:
            book_details['ISBN'] = book_details.pop("ISBN-13")
        return render_template("addstock.html", **book_details)

@app.route("/addstock", methods=["GET", "POST"])
@login_required
def addstock():
    """Get stock quote."""
    if request.method == "GET":
        # Display form for user to enter stock to search
        return render_template("add.html", book)
    else:
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        level = request.form.get("level")
        edition = request.form.get("edition")
        price_new = float(request.form.get("price_new"))
        price_used = float(request.form.get("price_used"))
        stock_new = request.form.get("stock_new")
        stock_used = request.form.get("stock_used")
        db.execute("INSERT INTO books(isbn, title, level, edition, stock_new, stock_used, price_new, price_used) VALUES(:isbn, :title, :level, :edition, :stock_new, :stock_used, :price_new, :price_used)",
                    isbn = isbn, title=title, level=level, edition=edition, stock_new=stock_new, stock_used=stock_used, price_new=price_new, price_used = price_used)
        flash("Title added")
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
