# CESBooks
A mini web application to manage an imaginary university library.
The application is written in Python using the Flask framework.


## Student Features
1. Login - secure password verified login.
2. Books - display all books in the library.
3. Borrow - borrow a book using barcode scanner.
4. Return - return a book using thebarcode scanner.
5. Account - display the user's borrowng history.

## Admin Features
1. Add Title - add new books to the database using the barcode scanner.
2. Books - display all books in the library.
3. Students - dispay all students, and the number of books each has on loan/overdue.
4. Current Loans - display all books currently on loan.
5. Overdue - display all books that are overdue.

## Integrations
1. The application integrates with a MySQL relational database.
2. The connection string is set in the application.py file.
3. Scripts to create the database schema can be found in the migrations folder.

## API
A REST API is exposed which allows other applications to create a new library account.
POST requests should be sent to /api/register, containing a JSON body { "studentId": "cXXXXXXX" } where cXXXXXXX is the student id. 
This results in a new library account with the default PIN '000000'.
Upon logging in for the first time, the new student will be asked to update this PIN.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
Copyright (c) 2020/21 A. Curley

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
