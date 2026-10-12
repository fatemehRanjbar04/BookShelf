from book import Book
from datetime import date
from project import finished_books_in_year
import pytest

def test_finished_books_in_year():
    
    assert finished_books_in_year(2026, []) == []
    
    book_1 = Book("The Stranger", "Albert Camus", "Novel", date(2026, 6, 1))
    assert finished_books_in_year(2026, [book_1]) == []
    
    book_2 = Book("The A.B.C Murders", "Agatha Christie", "Mystery", date(2025, 12, 12), date(2026, 2, 6))
    assert finished_books_in_year(2025, [book_2]) == []
    assert finished_books_in_year(2026, [book_2]) == ["The A.B.C Murders"]
    assert finished_books_in_year(2026, [book_1, book_2]) == ["The A.B.C Murders"]
    
    