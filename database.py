import sqlite3
from datetime import date
from book import Book

def create_table(database):
    database.execute(
        "CREATE TABLE IF NOT EXISTS books("
        "BookID INTEGER PRIMARY KEY, "
        "Title VARCHAR(255) NOT NULL, "
        "Author VARCHAR(255) NOT NULL, "
        "Genre VARCHAR(255) NOT NULL, "
        "StartDate DATE NOT NULL, "
        "EndDate DATE, "
        "Quote TEXT, "
        "Opinion TEXT)"
        )


def row_to_book(row):
    end_date = None
    if row["EndDate"] is not None:
        end_date = date.fromisoformat(row["EndDate"])
       
    book = Book(row["Title"], row["Author"], row["Genre"], date.fromisoformat(row["StartDate"]), 
                end_date, row["Quote"], row["Opinion"], row["BookID"])
    return book
    


def add_book(database, book): 
    start = book.start_date.isoformat()
    end = None
    if book.end_date is not None:
        end = book.end_date.isoformat()
    database.execute("""
               INSERT INTO books(
                Title, Author, Genre, StartDate, EndDate, Quote, Opinion) 
                VALUES (?,?,?,?,?,?,?)"""
               ,(book.title, book.author, book.genre, start, end, book.quote, book.opinion)) 
    
    database.commit()
             

def get_all_books(database):
    rows = database.execute("SELECT * FROM books ORDER BY BookID").fetchall()
    books = [row_to_book(r) for r in rows]
    return books
        

def connect_database(file):
    database = sqlite3.connect(file)
    create_table(database)
    database.row_factory = sqlite3.Row
    return database


def delete_book(database, book_id):
    result = database.execute("DELETE FROM books WHERE BookID = ?", (book_id,))
    database.commit()
    if result.rowcount:
        return True
    else:
        return False
    
def update_book(database, book):
    start = book.start_date.isoformat()
    end = None
    if book.end_date is not None:
        end = book.end_date.isoformat()
        
    update = database.execute("""UPDATE books SET Title = ?, Author = ?, Genre = ?, 
                     StartDate = ?, EndDate = ?, Quote = ?, Opinion = ?
                     WHERE BookID = ?""", (book.title, book.author, book.genre, start, 
                                           end, book.quote, book.opinion, book.book_id))
    
    database.commit()
    
    if update.rowcount:
        return True
    else:
        return False