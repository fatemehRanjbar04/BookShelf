from book import Book
from datetime import date
from project import finished_books_in_year, number_of_finished_books_in_year, average_reading_days, favorite_genres, get_most_reading_month, random_quote

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
    assert average_reading_days([book_1, book_2]) == 30.0
    book_3 = Book("The A.B.C Murders", "Agatha Christie", "Mystery", date(2025, 12, 12), date(2025, 12, 14))  
    assert average_reading_days([book_2, book_3]) == 16.5
    
def test_favorite_genres():
    assert favorite_genres([]) == []
    book_1 = Book("The Stranger", "Albert Camus", "Novel", date(2026, 6, 1))
    book_2 = Book("The A.B.C Murders", "Agatha Christie", "Mystery", date(2025, 12, 12), date(2026, 2, 6))
    book_3 = Book("The Stranger", "Albert Camus", "Novel", date(2026, 6, 1))
    book_4 = Book("The A.B.C Murders", "Agatha Christie", "Mystery", date(2025, 12, 12), date(2026, 2, 6))
    book_5 = Book("The Stranger", "Albert Camus", "...", date(2026, 6, 1)) 
    assert favorite_genres([book_1, book_2, book_3]) == ['Novel']
    assert favorite_genres([book_1, book_2, book_3, book_4, book_5]) == ['Novel', 'Mystery']
    
    
def test_get_most_reading_month():
    assert get_most_reading_month([]) == []
    book_1 = Book("The Stranger", "Albert Camus", "Novel", date(2026, 6, 1), date(2026, 6, 1))
    book_2 = Book("The A.B.C Murders", "Agatha Christie", "Mystery", date(2025, 12, 12), date(2026, 2, 6))
    book_3 = Book("...", "...", "...", date(2025, 12, 12), date(2026, 2, 10))
    book_4 = Book("...", "...", "...", date(2026, 6, 1), date(2026, 6, 1))
    book_5 = Book("...", "...", "...", date(2026, 6, 1))
    assert get_most_reading_month([book_1, book_2, book_3]) == [((2026, 2), ["The A.B.C Murders", "..."])]
    
    assert get_most_reading_month([book_1, book_2, book_3, book_4, book_5]) == [((2026, 2), ["The A.B.C Murders", "..."]),
                                                                                ((2026, 6), ["The Stranger", "..."])]
 
def test_random_quote():
    book_1 = Book("...", "...", "...", date(2026, 6, 1))
    book_2 = Book("The A.B.C Murders", "Agatha Christie", "Mystery", date(2025, 12, 12), quote="Test")
    book_3 = Book("...", "...", "...", date(2025, 12, 12))
    quotes = [book_1, book_2, book_3]
    assert random_quote(quotes) == ('Agatha Christie', 'Test')
    assert random_quote([]) is None
    assert random_quote([book_1, book_3]) is None