import re

FINE_PER_DAY = .50
MAX_BORROWING_DURATION = 14
MAX_PAYMENT_DURATION = 14
MAX_BOOKS_ALLOWED = 5
INVOICES_URL = "http://localhost:8081/invoices"

BOOK_NOT_FOUND_MESSAGE = 'This book is not in our database, or there may be an error in the ISBN.'


ISBN_PATTERN = re.compile(r'[\d]{13}')
PIN_PATTERN = re.compile(r'[\d]{6}')