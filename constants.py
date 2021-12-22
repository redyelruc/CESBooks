import re


FINE_AMOUNT_PER_DAY = .50
MAX_BORROWING_DURATION = 14
MAX_BOOKS_ALLOWED = 5
INVOICES_URL = "http://localhost:8081/invoices"


ISBN_PATTERN = re.compile(r'[\d]{13}')