# BookShelf

#### Video Demo: <URL HERE>

#### Description:

**BookShelf** is a personal library program that runs in the terminal. You can add the information of the books you read and keep everything in one place, so it works like your own private library.

I built it because of a habit I already had. Whenever I start a book, I write down its information and the date I started it. When I finish it, I write my opinion and the date I finished it. I kept these notes for a whole year, and I had to organize and arrange them by hand. Now BookShelf does this work for me. I can add, edit, and delete books, see the list of books I have read, and open the details of each book.

What makes it more interesting is the statistics. I can see a summary of my reading in a year.

## Features

When you run the program, it shows a menu in the terminal:

```
[1] Add a book
[2] Finish a book
[3] List books
[4] Edit a book
[5] Delete a book
[6] Statistics
[7] Quote of the Day!
[0] Quit
```

- **Add a book (1):** You can add a book you have just started reading. The end date, the quote, and your opinion are optional, so you can fill them in later.
- **Finish a book (2):** When you finish a book, you can add its end date, a quote, and your opinion. This option only shows the books that do not have an end date yet.
- **List books (3):** You can see all your books and their status (finished or still reading). You can also choose a book from the list to see its full details.
- **Edit a book (4):** You can edit all the information you entered for a book. For the end date, the quote, and the opinion, pressing Enter without typing anything leaves the value unchanged. The title, the author, the genre, and the start date cannot be empty.
- **Delete a book (5):** You can choose a book and delete it from your library and from the database. The program asks you to confirm before deleting.
- **Statistics (6):** You enter a year, and the program shows your reading statistics for that year: how many books you finished, the average number of days per book, your favorite genre, and the month in which you read the most books. It also shows a random quote from the books you finished that year.
- **Quote of the Day (7):** The program shows a random quote from your books, with the author's name.
- **Quit (0):** The program keeps running until you enter 0.

## Project Files

**`project.py`** is the main file, and it is the file you run. It contains the `main()` function, the terminal menu, and the functions behind each menu option: adding, finishing, listing, editing, and deleting books. It also contains the statistics functions: the books finished in a year, the average number of days per book, the favorite genre, the month with the most finished books, and a random quote. This file has to talk to the database and also create `Book` objects, so it imports from both `book.py` and `database.py`.

**`book.py`** contains the `Book` class. At first, I did not plan to put it in a separate file. But `project.py` was already long and full of functions, and I got confused when it became crowded. A separate file is much tidier, and it lets me test the class on its own. I also wanted to build a proper class.

A `Book` object has four required values (`title`, `author`, `genre`, `start_date`) and three optional values (`end_date`, `quote`, `opinion`). The class validates all the inputs, so a book with invalid data cannot be created. Dates must be `date` objects. The title, the author, and the genre must be strings and cannot be empty. They are saved with `.strip().title()`. The quote and the opinion are also stripped, and an empty text becomes `None`. The end date cannot be before the start date.

Besides the validation, the class has two important methods. `is_finished()` checks whether I finished reading the book, and `days_to_read()` calculates how many days it took to read it.

**`database.py`** contains everything about the database. I decided to add a database because I do not want my data to disappear when the program closes. Since this is a library, saving the books is the logical thing to do. All the operations are in this file: creating the table, adding, reading, updating, and deleting books. SQLite has no date type, so the dates are saved as text in the `YYYY-MM-DD` format and converted back to `date` objects when the books are read.

**`test_book.py`**, **`test_database.py`**, and **`test_project.py`** contain the automated tests (run with `pytest`). I wrote the tests for `Book` to make sure it works the way I want, and to find and fix bugs. `test_database.py` tests all the database operations, using a temporary database in memory instead of a real file. `test_project.py` tests the statistics functions.

**`requirements.txt`** lists the only library that needs to be installed with `pip`, which is `pytest`.

## How to Run

**Requirements:** Python 3.10 or newer. (The program uses the `match` statement, which does not exist in older versions.) The program itself only uses Python's built-in modules, so you do not need to install anything to run it. The only library you can install with `pip` is `pytest`, and it is used only for testing.

**1. (Optional) Create a virtual environment.** You can run the project without one, but it keeps your packages separate from other projects.

```
python -m venv venv
```

Activate it on Windows (PowerShell):

```
.\venv\Scripts\Activate.ps1
```

Or on macOS and Linux:

```
source venv/bin/activate
```

**2. Install `pytest`** (needed only to run the tests):

```
pip install -r requirements.txt
```

This is the same as running `pip install pytest`.

**3. Run the program** from the project folder:

```
python project.py
```

As soon as the program starts, it creates a file named `books.db` to save your books in a database. Then the menu appears and you can start using it.

**Important:** `books.db` is created in the folder you run the command from. Always run the program from the project folder. If you run it from another folder, it will create a new, empty `books.db` there, and your books will look like they are gone.

**4. Run the tests.** The tests are in three files: `test_book.py`, `test_database.py`, and `test_project.py`. To run all of them, type:

```
pytest
```

To run only one file, add its name:

```
pytest test_book.py
```

## Design Decisions

**A `Book` class instead of a dictionary.** I wanted to build a proper class, and it also helped me practice a part of Python where I felt weak. Because the class validates its own data, any `Book` that exists in the program is always valid, no matter where it was created.

**Required and optional values.** `title`, `author`, `genre`, and `start_date` are required, because the statistics depend on them: the favorite genre needs a genre, and the reading time and the list of unfinished books need a start date. `end_date`, `quote`, and `opinion` are optional, because when I start a book I have not finished it and I do not have an opinion yet. The price of this choice is that I cannot add an old book if I do not remember when I started it.

**Validation inside the class.** I put the rules inside `Book` (with properties and setters), not in the menu. This way, there is one place for the rules, and every route that changes a book, such as creating or editing, uses the same rules. The end date rule is also checked when the start date changes. An empty quote or opinion becomes `None`, so there is only one way to say that a value is missing.

**Two kinds of errors.** The validation raises `TypeError` when the type is wrong and `ValueError` when the value is wrong. I need to be sure that I receive exactly the type I expect, especially for dates, where I wanted real `date` objects and not strings. It also protects the code in the future: if someone changes the code and tries to pass an `int` where a `str` is required, the program fails immediately instead of saving bad data.

**A read-only `book_id`.** To edit or delete one book, the program must know which database row it is. So `Book` has an optional `book_id`. It has no setter, so nobody can change it by mistake and edit the wrong row.

**Counting the reading days.** `days_to_read()` calculates `(end_date - start_date).days + 1`. At first I did not write the `+ 1`, but my tests showed me a problem: a book that I start and finish on the same day took 0 days. That is not logical, because I did spend time reading it, and it would also make my averages wrong. With `+ 1`, both the first day and the last day are counted, so a one-day book takes 1 day.

**Statistics functions only receive a list.** The statistics functions do not talk to the database. They only receive a list of `Book` objects and return a result. This makes them easy to test, because I can build a small list of books by hand and check the answer without creating a database. It also keeps the functions simple and separate from the database code.

**Filtering with Python, not SQL.** The filters in the statistics (for example, the books finished in a given year) are done in Python on the list of books. A personal library is small, so speed is not a problem. Doing the filtering in Python also means that I can test it without a database, and the SQL in `database.py` stays simple.

**Passing the database connection as a parameter.** Some functions need the books that are stored in the library. For example, when the user chooses a book to edit or delete, the program must read the saved books. For these functions, I pass the database connection as a parameter instead of creating it inside each function. This has three advantages. First, the connection is created once in `main()` and closed when the user quits. Second, the functions are easy to test: in the tests, I pass a temporary database in memory (`":memory:"`), so the tests never touch the real `books.db`, and every test starts with an empty database. Third, the same function works with any database, so nothing in the code is tied to one file.

**SQL decisions.** I always use placeholders (`?`) and never put the user's text directly into an SQL command, to avoid SQL injection. I use `sqlite3.Row`, so I read columns by name instead of by position, and a change in the column order cannot break the code silently. `connect_database()` creates the table (with `IF NOT EXISTS`) and sets the row factory in one place, so I cannot forget it. `update_book()` always writes all the fields: the program first reads the book, changes it (the setters validate every change), and then saves it. `update_book()` and `delete_book()` return `True` or `False`, depending on whether a row was really changed.

**Asking again until the input is correct.** The program accepts inputs only in a specific format (for example, dates as `YYYY-MM-DD`), so that everything works the way the program was written. The format is shown to the user when the program asks. If the user enters a wrong value, the program shows a message and asks again, until the input is correct. The validation rules live in the `Book` class, and the menu only reuses them.

**What "statistics for a year" means.** I count the books that I finished in that year, because the average reading time and the busiest month only make sense for finished books. When two genres or two months are tied, the functions return all of them, in chronological order for months, so the result never depends on the order of the books. If there is no data, they return `None` or an empty list, and the menu shows a clear message instead of failing. The random quote only chooses from books that have a quote.

**How the menu looks.** The table has fixed column widths and shortens long text with "…", so the columns stay aligned. The full details of a book are shown separately, when the user chooses a book from the list, and long quotes and opinions are wrapped with `textwrap`. Deleting a book asks for confirmation. When editing, an empty answer for an optional value means "no change", which means that a quote or an opinion cannot be erased. I also capitalize titles, authors, and genres with `.title()`. I know it has small mistakes, like "Don'T", but I accepted them to keep the code simple.

**The database file location.** I decided not to fix the location of `books.db`. The file is created in the folder where the program is run. I knew that a fixed location (using the `pathlib` module) would remove the problem that running the program from another folder creates a new, empty database. But for this first version, I felt that the project already did what I needed, and I preferred to keep it simple. I accept this as a known limitation, so I explain it in the "How to Run" section: always run the program from the project folder.

**Testing.** I test the logic functions with small lists of books that I create by hand, and the database functions with a temporary database in memory. The tests in `test_project.py` are named `test_` plus the name of the function they test, as the CS50 rules require. Functions that use `input()` are tested by hand, not automatically. The `.gitignore` file ignores `*.db` files, so my personal notes never go to GitHub.
