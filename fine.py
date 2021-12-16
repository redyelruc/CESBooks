from datetime import timedelta, date
from helpers import days_between


class Fine:
    def __init__(self, amount_per_day, due_date, student_id):
        self.amount = amount_per_day * days_between(due_date, date.today())
        self.dueDate = date.today() + timedelta(days=14)
        self.type = 'LIBRARY_FINE'
        self.student_id = {'studentId': student_id}
        self.details = {'amount': self.amount, 'due': self.dueDate, 'type': self.type, 'account': self.student_id}
