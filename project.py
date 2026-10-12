from book import Book
from datetime import date
from collections import Counter
import random

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
    if count == 0:
        return None
    else:
        return round((total/count), 1)
   
    
def favorite_genres(books):
    genres = [book.genre for book in books]

    count = Counter(genres).most_common() 
    favorite = []    
    for i in count:
        if i[1] == count[0][1]:
            favorite.append(i[0])
    return favorite



def get_most_reading_month(books):
    count = [(book.title, book.end_date) for book in books if book.is_finished()]
    months = {}
    for i in count:
        key = (i[1].year, i[1].month)
        if key in months:
            value = months[key]
            value.append(i[0])
        else:
            value = []
            value.append(i[0])
            months[key] = value
            
    temp = 0
    title = []
    best_month = []
    for m in sorted(months):
        if temp < (len(months[m])):
            temp = len(months[m])
            title = [months[m]]
            best_month = [m]         
        elif temp == len(months[m]):
            title.append(months[m])
            best_month.append(m)
            
    return list(zip(best_month, title))
    
    
def random_quote(books):
    quotes = [(book.author, book.quote) for book in books if book.quote is not None]
    if quotes:
        selected_quote = random.choice(quotes)
    else:
        selected_quote = None
    return selected_quote
            
    

if __name__ == "__main__":
    main()