import sqlite3
from datetime import date
from book import Book


def create_table(database):
    database.execute(
        "CREATE TABLE IF NOT EXISTS books("
        "BookID INTEGER PRIMARY KEY, "
        "Title VARCHAR(255) NOT NULL, "
        "Author VARCHAR(255) NOT NULL, "
        "Genre VARCHAR(255) NOT NULL, "
        "StartDate DATE NOT NULL, "
        "EndDate DATE, "
        "Quote TEXT, "
        "Opinion TEXT)"
        )


def row_to_book(row):
    end_date = None
    if row["EndDate"] is not None:
        end_date = date.fromisoformat(row["EndDate"])
       
    book = Book(row["Title"], row["Author"], row["Genre"], date.fromisoformat(row["StartDate"]), 
                end_date, row["Quote"], row["Opinion"])
    return book
    



