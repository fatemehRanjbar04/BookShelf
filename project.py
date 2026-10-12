from book import Book
from datetime import date

def finished_books_in_year(year, books):
    result = []
    for book in books:
        if book.is_finished() and book.end_date.year == year:
            result.append(book.title)
    return result