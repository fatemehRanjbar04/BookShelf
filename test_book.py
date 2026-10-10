import pytest
from book import Book
from datetime import date

def test_book():
    book = Book("The Stranger", "Albert Camus", "Novel", date(2026, 6, 1))
    assert str(book) == "Book: The Stranger\nAuthor: Albert Camus\nGenre: Novel"
    
    book = Book("   The Stranger   ", "Albert Camus   ", "  Novel", date(2026, 6, 1)) 
    assert str(book) == "Book: The Stranger\nAuthor: Albert Camus\nGenre: Novel"
   
      
def test_validate_str():      
    with pytest.raises(ValueError):
        Book(" ", "Albert Camus", "Novel", date(2026, 6, 1))
    
    with pytest.raises(ValueError):
        Book("The Stranger", "  ", "Novel", date(2026, 6, 1))

    with pytest.raises(ValueError):
        Book("The Stranger", "", "Novel", date(2026, 6, 1))
              
    with pytest.raises(ValueError):
        Book("The Stranger", "Albert Camus", " ", date(2026, 6, 1))

    with pytest.raises(TypeError):
        Book(10, "Albert Camus", "Novel", date(2026, 6, 1))
        
    with pytest.raises(TypeError):
        Book("The Stranger", 20, "Novel",date(2026, 6, 1))   
        
    with pytest.raises(TypeError):
        Book("The Stranger", "Albert Camus", 30 , date(2026, 6, 1))
 
         
def test_validate_optional_text():
    book = Book("The Stranger", "Albert Camus", "Novel", date(2026, 6, 1), date(2026, 8, 1), " ")
    assert book.quote is None
    book.quote = "   Hello "
    assert book.quote == "Hello"  
    with pytest.raises(TypeError):
        book.quote = 5
        
    book = Book("The Stranger", "Albert Camus", "Novel", date(2026, 6, 1), date(2026, 8, 1), " ", "")   
    assert book.opinion is None
    book.opinion = "I liked it.   "
    assert book.opinion == "I liked it."  
    with pytest.raises(TypeError):
        book.opinion = 5
    
              
def test_validate_date():   
    book = Book("The Stranger", "Albert Camus", "Novel", date(2026, 8, 29), date(2026, 9, 10))

    assert book.start_date == date(2026, 8, 29)
    assert book.end_date == date(2026, 9, 10)

    book = Book("The Stranger", "Albert Camus", "Novel",date(2026, 8, 29))
    assert book.end_date is None
    
    book = Book("The Stranger", "Albert Camus", "Novel", date(2026, 8, 29), date(2026, 8, 29))
    assert book.start_date == book.end_date

    with pytest.raises(TypeError):
        Book("The Stranger", "Albert Camus", "Novel", "2026-08-29")

    with pytest.raises(TypeError):
        Book("The Stranger", "Albert Camus", "Novel", date(2026, 8, 29), "2026-08-30")

    with pytest.raises(ValueError):
        Book("The Stranger", "Albert Camus", "Novel", date(2026, 10, 29), date(2026, 8, 1))
        
    book = Book("The Stranger", "Albert Camus", "Novel", date(2026, 1, 1), date(2026, 2, 1))
    with pytest.raises(ValueError):
        book.start_date = date(2026, 5, 10) 
 
def test_is_finished():
    book = Book("The Stranger", "Albert Camus", "Novel", date(2026, 1, 1), date(2026, 2, 1))
    assert book.is_finished() == True
    
    book = Book("The Stranger", "Albert Camus", "Novel", date(2026, 1, 1))
    assert book.is_finished() == False
    
def test_days_to_read():
    book = Book("The Stranger", "Albert Camus", "Novel", date(2026, 1, 1), date(2026, 1, 10))
    assert book.days_to_read() == 10
