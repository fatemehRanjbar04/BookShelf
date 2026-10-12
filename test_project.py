from book import Book
from datetime import date
from project import finished_books_in_year, number_of_finished_books_in_year, average_reading_days
import pytest

def test_finished_books_in_year():   
    assert finished_books_in_year(2026, []) == []
    book_1 = Book("The Stranger", "Albert Camus", "Novel", date(2026, 6, 1))
    assert finished_books_in_year(2026, [book_1]) == []
    book_2 = Book("The A.B.C Murders", "Agatha Christie", "Mystery", date(2025, 12, 12), date(2026, 2, 6))
    assert finished_books_in_year(2025, [book_2]) == []
    assert finished_books_in_year(2026, [book_2]) == ["The A.B.C Murders"]
    assert finished_books_in_year(2026, [book_1, book_2]) == ["The A.B.C Murders"]
    
  
def test_number_of_finished_books_in_year():
    assert number_of_finished_books_in_year(2026, []) == 0
    book_1 = Book("The Stranger", "Albert Camus", "Novel", date(2026, 6, 1))
    book_2 = Book("The A.B.C Murders", "Agatha Christie", "Mystery", date(2025, 12, 12), date(2026, 2, 6))
    assert number_of_finished_books_in_year(2026, [book_1, book_2]) == 1
    
    
def test_average_reading_days():
    assert average_reading_days([]) == None
    book_1 = Book("The Stranger", "Albert Camus", "Novel", date(2026, 6, 1))
    assert average_reading_days([book_1]) == None
    book_2 = Book("The Stranger", "Albert Camus", "Novel", date(2026, 6, 1), date (2026, 6, 30))
    assert average_reading_days([book_2]) == 30.0