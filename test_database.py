from database import add_book, get_all_books, connect_database, delete_book, update_book
from datetime import date
from book import Book
import pytest

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
    
    

def test_book_quote_and_opinion():
    database = connect_database(":memory:")
    book = Book("The Stranger", "Albert Camus", "Novel", date(2026, 2, 10), date(2026, 2, 17),
                "Today, mother died", "Thoughtful")

    add_book(database, book)
    books = get_all_books(database)
    assert len(books) == 1
    assert books[0].quote == "Today, mother died"
    assert books[0].opinion == "Thoughtful"


def test_book_without_id():
    book = Book("book1", "writer", "...", date(2026, 8, 29))
    assert book.book_id is None


def test_book_with_id():
    book = Book("book1", "writer", "...", date(2026, 8, 29), book_id=5)
    assert book.book_id == 5
    
    with pytest.raises(AttributeError):
        book.book_id = 5

def test_bookID():
    database = connect_database(":memory:")
    book = Book("book1", "writer", "...", date(2026, 8, 29))
    add_book(database, book)
    book = Book("book2", "writer2", "...", date(2026, 8, 30))
    add_book(database, book)
    books = get_all_books(database)
    assert books[0].book_id == 1
    assert books[1].book_id == 2


def test_delete_book():
    database = connect_database(":memory:")
    assert delete_book(database, 1) == False
    
    add_book(database, Book("book1", "writer", "...", date(2026, 8, 29)))
    add_book(database, Book("book2", "writer2", "...", date(2026, 8, 30)))
    assert delete_book(database, 1) == True
    
    books = get_all_books(database)
    assert books[0].book_id == 2
    assert len(books) == 1
    assert delete_book(database, 1) == False
    
    
def test_update_book():
    database = connect_database(":memory:")  
    add_book(database, Book("book1", "writer", "...", date(2026, 8, 29)))
    add_book(database, Book("book2", "writer2", "...", date(2026, 8, 30)))
    books = get_all_books(database)
    books[0].genre = "Novel"
    assert update_book(database, books[0]) is True
    update_books = get_all_books(database)
    assert update_books[0].genre == "Novel"
    assert update_books[1].genre == "..."
    
    
    add_book(database, Book("book3", "writer3", "...", date(2026, 8, 31), quote="This is a Test."))
    books = get_all_books(database)
    books[2].quote = None
    books[2].end_date = date(2026, 9, 7)
    assert update_book(database, books[2]) is True
    update_books = get_all_books(database)
    assert update_books[2].quote is None
    assert update_books[2].end_date == date(2026, 9, 7)
    
    
    missing_book = Book("new", "unknown", "historical", date(2024, 8, 31), book_id=10)
    assert update_book(database, missing_book) is False
    assert len(get_all_books(database)) == 3