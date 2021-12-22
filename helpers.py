import re
from datetime import date
from flask import redirect, render_template, session
from functools import wraps

from constants import ISBN_PATTERN


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def days_between(d1, d2):
    return abs((d2 - d1).days)


def is_overdue(date_borrowed, date_returned):
    if date_returned is not None:
        return ''
    days_borrowed = days_between(date_borrowed, date.today())
    if days_borrowed < 14:
        return ''
    return f'{days_borrowed - 14} days'


def is_valid_isbn(isbn):
    if re.fullmatch(ISBN_PATTERN, isbn) is None:
        raise ValueError('The ISBN must contain 13 digits.')
    else:
        return isbn


def is_valid_year(year):
    try:
        year_int = int(year)
    except ValueError:
        raise ValueError('Invalid year.')
    if 1500 <= year_int <= date.today().year:
        return year
    else:
        raise ValueError('Invalid year.')


def is_valid_num_copies(copies):
    try:
        num_copies = int(copies)
    except ValueError:
        raise ValueError('Invalid number of copies.')
    if 100 < num_copies > 0:
        return copies
    else:
        raise ValueError('Invalid number of copies.')
