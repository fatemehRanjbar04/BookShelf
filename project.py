from book import Book
from datetime import date

def main():
    ...

def finished_books_in_year(year, books):
    result = []
    for book in books:
        if book.is_finished() and book.end_date.year == year:
            result.append(book.title)
    return result


def number_of_finished_books_in_year(year, books):
    result = finished_books_in_year(year, books)
    return len(result)


def average_reading_days(books):
    total = 0
    count = 0
    for book in books:
        if book.is_finished():
            total += book.days_to_read()
            count += 1      
    if total == 0:
        return None
    else:
        return round((total/count), 1)
    
 
 
  
  
  
    
if __name__ == "__main__":
    main()