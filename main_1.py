from tkinter import *
from library import Library
import requests
from datetime import date, timedelta

# Create a new library
my_library = Library()

# Add some books to the library
my_library.add_book("The Great Gatsby", "F. Scott Fitzgerald", 5)
my_library.add_book("To Kill a Mockingbird", "Harper Lee", 3)
my_library.add_book("1984", "George Orwell", 7)
my_library.add_book("Pride and Prejudice", "Jane Austen", 2)

# Add some members to the library
my_library.add_member("John Doe", "jdoe@example.com", "555-1234")
my_library.add_member("Jane Smith", "jsmith@example.com", "555-5678")

# Issue a book to a member
my_library.issue_book("The Great Gatsby", "John Doe")

# Return a book from a member
my_library.return_book("The Great Gatsby", "John Doe")

# Search for a book by name and author
my_library.search_books("To Kill a Mockingbird", "Harper Lee")

# Import books from Frappe API
my_library.import_books_from_api("Harry Potter", 10)

# View all books in the library
my_library.view_books()

# View all members in the library
my_library.view_members()

# Delete a book from the library
my_library.delete_book("1984")

# Delete a member from the library
my_library.delete_member("Jane Smith")


class LibraryManagementGUI:
    def __init__(self, library):
        self.library = library
        self.window = Tk()
        self.window.title("Library Management System")
        self.window.geometry("800x600")

        # create labels
        Label(self.window, text="Book Title").grid(row=0, column=0)
        Label(self.window, text="Author").grid(row=1, column=0)
        Label(self.window, text="Stock").grid(row=2, column=0)
        Label(self.window, text="Member ID").grid(row=4, column=0)
        Label(self.window, text="Book ID").grid(row=5, column=0)

        # create entry fields
        self.book_title_entry = Entry(self.window)
        self.book_title_entry.grid(row=0, column=1)
        self.author_entry = Entry(self.window)
        self.author_entry.grid(row=1, column=1)
        self.stock_entry = Entry(self.window)
        self.stock_entry.grid(row=2, column=1)
        self.member_id_entry = Entry(self.window)
        self.member_id_entry.grid(row=4, column=1)
        self.book_id_entry = Entry(self.window)
        self.book_id_entry.grid(row=5, column=1)

        # create buttons
        Button(self.window, text="Add Book", command=self.add_book).grid(row=3, column=0)
        Button(self.window, text="Update Book", command=self.update_book).grid(row=3, column=1)
        Button(self.window, text="Delete Book", command=self.delete_book).grid(row=3, column=2)
        Button(self.window, text="Search Book", command=self.search_books).grid(row=3, column=3)
        Button(self.window, text="Issue Book", command=self.issue_book).grid(row=6, column=0)
        Button(self.window, text="Return Book", command=self.return_book).grid(row=6, column=1)
        Button(self.window, text="Import Books", command=self.import_books).grid(row=6, column=2)

        # create listbox
        self.books_listbox = Listbox(self.window, width=80)
        self.books_listbox.grid(row=7, column=0, columnspan=4)

        # display all books
        self.display_books()

        # start GUI
        self.window.mainloop()
class Book:
    def __init__(self, book_id, name, author, stock):
        self.book_id = book_id
        self.name = name
        self.author = author
        self.stock = stock

class Transaction:
    def __init__(self, member_id, book_id, issue_date, due_date):
        self.member_id = member_id
        self.book_id = book_id
        self.issue_date = issue_date
        self.due_date = due_date
        self.return_date = None
        self.fee = 0
    def add_book(self):
        book_title = self.book_title_entry.get()
        author = self.author_entry.get()
        stock = int(self.stock_entry.get())
        self.library.add_book(book_title, author, stock)
        self.display_books()

    def update_book(self):
        book_id = int(self.book_id_entry.get())
        book_title = self.book_title_entry.get()
        author = self.author_entry.get()
        stock = int(self.stock_entry.get())
        self.library.update_book(book_id, book_title, author, stock)
        self.display_books()

    def delete_book(self):
        book_id = int(self.book_id_entry.get())
        self.library.delete_book(book_id)
        self.display_books()

    def search_books(self):
        book_title = self.book_title_entry.get()
        author = self.author_entry.get()
        books = self.library.search_books(book_title, author)
        self.display_books(books)

    def issue_book(self):
        book_id = int(self.book_id_entry.get())
        member_id = int(self.member_id_entry.get())
        self.library.issue_book(book_id, member_id)
        self.display_books()

    def return_book(self, member_id, book_id, return_date):
        for transaction in self.transaction_list:
            if transaction.member_id == member_id and transaction.book_id == book_id and transaction.return_date is None:
                transaction.return_date = return_date
                days_late = (return_date - transaction.due_date).days
                if days_late > 0:
                    transaction.fee = min(days_late * 500, 500)
                for book in self.book_list:
                    if book.book_id == book_id:
                        book.stock += 1
                return True
        return False
    
class Member:
    def __init__(self, member_id, name, address, phone_number, outstanding_debt):
        self.member_id = member_id
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.outstanding_debt = outstanding_debt    

class Library:
    def __init__(self):
        self.book_list = []

    def import_books(self, title, author, publisher, num_books):
        url = "https://frappe.io/api/method/frappe-library?page=2&title=and"
        payload = {
            "title": title,
            "author": author,
            "publisher": publisher,
            "num_books": num_books
        }
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            result = response.json().get('result')
            if result:
                for book in result:
                    new_book = Book(book.get('title'), book.get('author'), book.get('publisher'), book.get('stock'))
                    self.book_list.append(new_book)
                return True
        return False

    def add_member(self, name, address, phone):
        new_member = Member(name, address, phone)
        self.member_list.append(new_member)

    def search_book(self, query):
        results = []
        for book in self.book_list:
            if query.lower() in book.title.lower() or query.lower() in book.author.lower():
                results.append(book)
        return results

    def issue_book(self, book_id, member_id):
        book = self.get_book_by_id(book_id)
        member = self.get_member_by_id(member_id)
        if book and member and book.stock > 0:
            book.stock -= 1
            transaction = Transaction(book_id, member_id, datetime.now())
            self.transaction_list.append(transaction)
            return True
        return False

    def return_book(self, book_id, member_id):
        book = self.get_book_by_id(book_id)
        member = self.get_member_by_id(member_id)
        if book and member:
            transaction = self.get_transaction(book_id, member_id)
            if transaction:
                transaction.return_date = datetime.now()
                days_late = (transaction.return_date - transaction.issue_date).days - 14
                if days_late > 0:
                    member.outstanding_debt += 500 * days_late
                book.stock += 1
                return True
        return False

    def get_book_by_id(self, book_id):
        for book in self.book_list:
            if book.id == book_id:
                return book
        return None

    def get_member_by_id(self, member_id):
        for member in self.member_list:
            if member.id == member_id:
                return member
        return None

    def get_transaction(self, book_id, member_id):
        for transaction in self.transaction_list:
            if transaction.book_id == book_id and transaction.member_id == member_id and not transaction.return_date:
                return transaction
        return None
    def update_member(self, member_id, updated_member):
        for i, member in enumerate(self.members):
            if member.member_id == member_id:
                self.members[i] = updated_member
                return True
        return False
    
    def delete_member(self, member_id):
        for i, member in enumerate(self.members):
            if member.member_id == member_id:
                del self.members[i]
                return True
        return False

