from database import add_book, get_all_books, connect_database
from datetime import date
from book import Book

def test_db_empty():
    database = connect_database(":memory:")
    assert get_all_books(database) == []
    
    
def test_db_add():
    database = connect_database(":memory:")
    book = Book("The Stranger", "Albert Camus", "Novel", date(2026, 2, 10), date(2026, 2, 17))
    add_book(database, book)
    books = get_all_books(database)
    assert len(books) == 1
    assert books[0].title == "The Stranger"
    assert books[0].author == "Albert Camus"
    assert books[0].genre == "Novel"
    assert books[0].start_date == date(2026, 2, 10)
    assert books[0].end_date == date(2026, 2, 17)
    assert books[0].quote is None
    assert books[0].opinion is None
    
    
    
def test_db_add_without_end_date():
    database = connect_database(":memory:")
    book = Book("The test", "Testify", "...", date(2026, 8, 29))
    add_book(database, book)
    
    books = get_all_books(database)
    assert len(books) == 1
    assert books[0].title == "The test"
    assert books[0].author == "Testify"
    assert books[0].genre == "..."
    assert books[0].start_date == date(2026, 8, 29)
    assert books[0].end_date is None
    assert books[0].quote is None
    assert books[0].opinion is None



def test_add_with_order():
    database = connect_database(":memory:")
    book = Book("book1", "writer", "...", date(2026, 8, 29))
    add_book(database, book)
    
    book = Book("book2", "writer2", "...", date(2026, 8, 30))
    add_book(database, book)
    
    books = get_all_books(database)
    
    assert len(books) == 2
    assert books[0].title == "book1"
    assert books[1].title == "book2"  