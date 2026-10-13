from book import Book
from datetime import date
from collections import Counter
import random
from database import connect_database, get_all_books, add_book, update_book, delete_book
import calendar

def main():
    database = connect_database("books.db")
    run_menu(database)
    

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
            
 
    
def run_menu(database):
    while True:
        print("""
╔════════════════════════════════════════╗
║           ✨ BOOKSHELF ✨              ║
║       Your personal library 📚☕       ║
╚════════════════════════════════════════╝
        ₊˚⊹♡   WELCOME!   ₊˚⊹♡
            
    [1] Add a book
    [2] Finish a book
    [3] List books
    [4] Edit a book
    [5] Delete a book
    [6] Statistics
    [7] Quote of the Day!
    [0] Quit""")
        n = input("\n୨୧ Choose an option ୨୧ : ").strip()
        
        match n:
            case "0":
                print("See you next time!💫\n")
                database.close()
                break
            case "1":
                add_book_flow(database)
                print("\n୨୧ ── ⋆⋅☆⋅⋆ ── ୨୧ YOUR BOOK ADDED SUCCESSFULLY 🔖୨୧ ── ⋆⋅☆⋅⋆ ── ୨୧\n")
                input("୨୧ Press Enter To Continue ୨୧")
                    
            case "2":
                finish_book_flow(database)
                print("\n୨୧ Press Enter To Continue ୨୧")
                
            case "3":
                books = get_all_books(database)
                if books == []:
                    print("Database is empty :(\nYou Haven't Added any books yet... ")
                    input("୨୧ Press Enter To Continue ୨୧")
                else:   
                    print("\n✦.⁺.✦.⁺ YOUR LIBRARY ✦.⁺. ✦.⁺")
                    show_books(books)                                        
                    input("\n୨୧ Press Enter To Continue ୨୧")
                    
            case "4":
                print("Which book do you want to edit?")
                book = choose_book_to_edit(database)
                edit_book(database, book)
                input("\n୨୧ Press Enter To Continue ୨୧")
                
            case "5":
                print("Which book do you want to delete?")
                book = choose_book_to_edit(database)
                if book:
                    user_input = input(f"Are you sure you want to DELETE {book.title}? [Y/N]: ").strip().lower()
                    if user_input == "y":
                        if delete_book(database, book.book_id):
                            print("₊˚⊹♡✧ Book Delete Successfully! ₊˚⊹♡✧")
                
            case "6":
                books = get_all_books(database)
                year = int(input("Which year statistics do you want? "))
                show_statistics(year, books)
                input("\n୨୧ Press Enter To Continue ୨୧")
                  
            case "7":
                books = get_all_books(database)
                r = random_quote(books) 
                if r is not None:
                    author, quote = r 
                    print(f"\n💌 You Highlighted Once:\n{quote}\n \033[3m by {author}✍️\033[0m\n")
                else:
                    print("You Haven't Saved Any Quotes Yet...\n")
                
                input("୨୧ Press Enter To Continue ୨୧")
                
            case _:
                print("Oops!Invalid Option :(\ntry again...\n")
                input("୨୧ Press Enter To Continue ୨୧")
                
    
       
# For case 1 Add Books   
# Lable = Title, Author, Genre  
def ask_required_text(label):
    while True:
        text = input(f"Enter book's {label}: ")
        try:
            Book.validation_str(text)
        except ValueError:
            print(f"{label} can't be empty! Try Again...") 
            continue      
        
        return text

# Prompt = Start Date        
def ask_start_date(prompt):
    while True: 
        start = input(f"Enter book's {prompt} (YYYY-MM-DD): ").strip()
        try:
            start_date = date.fromisoformat(start)
        except ValueError:
            print(f"{start} is a wrong format for a date! Try Again...")
            continue
        return start_date    
 
# Prompt = End Date
def ask_end_date(prompt, start):
    print("If you have read this book completely enter the finished date. Else Enter to continue...")
    while True:
        end = input(f"Enter book's {prompt} (YYYY-MM-DD): ").strip()
        if end.strip() == "":
            return None 
        try:
            end_date = date.fromisoformat(end)
        except ValueError:
            print(f"{end} is a wrong format for a date! Try Again...")
            continue
        try:
            Book.validation_end_date(start, end_date)
        except ValueError:
            print("End date can't be before start date! Try Again...")
            continue
            
        return end_date            
            
# prompt = Quote, Opinion
def ask_optional_text(prompt) :
    print(f"If you have {prompt} for this book enter. Else Enter to continue...")
    text = input(f"Enter Your {prompt}: ")
    return Book.validation_optional_text(text)
          
# Add book case 1    
def add_book_flow(database):
    title = ask_required_text('Title')
    author = ask_required_text('Author')
    genre = ask_required_text('Genre')
    start_date = ask_start_date('Start Date')
    end_date = ask_end_date('End Date', start_date)
    quote = ask_optional_text('Quote')
    opinion = ask_optional_text('Opinion')
    
    book = Book(title, author, genre, start_date, end_date, quote, opinion)
    add_book(database, book)
 
 
 
 
#For Case 2 Finish Book
def choose_unfinished_book(books):
    unfinished_books = []
    for book in books:
        if not book.is_finished():
            unfinished_books.append(book) 
    if unfinished_books == []:   
        return None   
    else:  
        show_books(unfinished_books)
        
        while True:
            try:
                book_id = int(input("Enter Book's ID: "))         
            except ValueError:
                print("You should input a Number!")
                continue
            
            for book in unfinished_books:
                if book_id == book.book_id:
                    return book
            print("Wrong ID! Try Again...")
            continue


def finish_book_flow(database):
    books = get_all_books(database)
    book = choose_unfinished_book(books)
    if book is None:
        print("⭐ You have no unfinished books ⭐")
    else:
        start = book.start_date
        print(f"You Started this book at {start}")
        end = ask_end_date('End Date', start)
        quote = ask_optional_text('Quote')
        opinion = ask_optional_text('Opinion')
        if end:
            book.end_date = end
            print("୨୧ ── ⋆⋅☆⋅⋆ ── ୨୧ Book marked as finished! ୨୧ ── ⋆⋅☆⋅⋆ ── ୨୧")
                           
        if quote:
            book.quote = quote
            print("୨୧ ── ⋆⋅☆⋅⋆ ── ୨୧ Quote saved successfully! ୨୧ ── ⋆⋅☆⋅⋆ ── ୨୧")
          
        if opinion:
            book.opinion = opinion
            print("୨୧ ── ⋆⋅☆⋅⋆ ── ୨୧ Opinion saved successfully! ୨୧ ── ⋆⋅☆⋅⋆ ── ୨୧")
            
        if end or quote or opinion:
            update_book(database, book)
        else:
            print("No changes made")



# For case 3 List Books 
def show_books(books):
    print("""                                  
ID     Title                        Author                  Genre               Status
───    ─────────────────────────    ────────────────────    ───────────────    ────────""")
    for book in books:
        if book.is_finished():
            status = "Finished"
        else:
            status = "Reading"                
        print(f"{book.book_id:<7}{shorten(book.title, 25):<29}{shorten(book.author, 20):<24}{shorten(book.genre, 15):<19}{status:<8}")
 
                             
def shorten(text, width):
    if len(text) > width:
        return text[:width-1]+"…"  
    else:
        return text 
 
 

# For case 4
def choose_book_to_edit(database):
    books = get_all_books(database)
    if books:
        show_books(books)
        while True:
            try:
                book_ID = int(input("Enter Book's ID: "))         
            except ValueError:
                print("You should input a Number!")
                continue      
            for b in books:
                if book_ID == b.book_id:
                    return b
            print("Wrong ID! Try Again...")
            continue
    else:
        print("You don't have any books in this Library. Continue to add one...\n")
        input("୨୧ Press Enter To Continue ୨୧")
 
    
def edit_book(database, book):
    while True:
        print("💡What do you want to edit in this book? ")
        valid_input = ["title", "author", "genre", "start date", "end date"]
        edit = input("choose between:\ntitle, author, genre, start date, end date: ").lower()
        
        if edit in valid_input:
            if edit == "title":
                title = ask_required_text('Title')
                book.title = title

            elif edit == "author":    
                author = ask_required_text('Author')
                book.author = author
          
            elif edit == "genre":    
                genre = ask_required_text('Genre')
                book.genre = genre
              
            elif edit == "start date":
                start_date = ask_start_date('Start Date')
                if book.is_finished():
                    if start_date <= book.end_date:
                        book.start_date = start_date
                    else:
                        print("The Start date is after End date! Try Again...")
                        continue
                else:
                    book.start_date = start_date
                
            elif edit == "end date":
                end_date = ask_end_date('End date', book.start_date)
                if end_date is not None:
                    book.end_date = end_date
                
        else:
            print("Invalid!! Try Again...")
            continue

        again = input("Do you want to continue changing? [Y/N] ").lower()
        if again == "y":
            continue
        elif again == "n":
            update_book(database, book)
            return "₊˚⊹♡✧ Your changes saved successfully! ₊˚⊹♡✧"        
 
 
def show_statistics(year, books):  
    n = number_of_finished_books_in_year(year, books)
    ave = average_reading_days(books)
    genres = favorite_genres(books)
    genres_text = ", ".join(genres)
    months = get_most_reading_month(books)
    reading_months = []  
    for m, title in months:
        year, month = m
        month_name = calendar.month_abbr[month]
        n_books = len(title)
        reading_months.append(f"{month_name} {year} ({n_books} books)")   
        
    busiest_month = ", ".join(reading_months)
      
    print(f"""
📊 Statistics for {year}
──────────────────────────────────────────────────────
  Books finished        : {n}
  Average reading time  : {ave} days
  Favorite genre        : {genres_text}
  Busiest month         : {busiest_month}
  
""")
    r = random_quote(books) 
    if r is not None:
        author, quote = r 
        print(f"    💬'{quote}'\n   — {author}")
    
    
if __name__ == "__main__":
    main()