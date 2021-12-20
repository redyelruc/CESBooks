from datetime import timedelta, date
from helpers import days_between
from constants import *

class Fine:
    def __init__(self, borrowed, student_id):
        self.days_borrowed = days_between(borrowed, date.today())
        self.amount = FINE_AMOUNT_PER_DAY * days_between(borrowed + timedelta(days=MAX_BORROWING_DURATION), date.today())
        self.dueDate = date.today() + timedelta(days=14)
        self.type = 'LIBRARY_FINE'
        self.student_id = {'studentId': student_id}
        self.details = {'amount': self.amount, 'due': self.dueDate, 'type': self.type, 'account': self.student_id}
