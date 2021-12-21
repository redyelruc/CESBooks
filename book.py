from errors import IncompleteBookError


class Book:
    def __init__(self, *args):
        if len(args) == 1:
            self.isbn = args[0]['isbn']
            self.title = args[0]['title']
            self.author = args[0]['author']
            self.year = args[0]['year']
            self.copies = args[0]['copies']
        else:
            self.isbn = args[0]
            self.title = args[1]
            self.author = args[2]
            self.year = args[3]
            self.copies = args[4]
