from datetime import date

class Book:
    def __init__(self, title, author, genre, start_date, end_date=None, 
                 quote=None, opinion=None, book_id=None):
        self.title = title
        self.author = author
        self.genre = genre
        self.start_date = start_date
        self.end_date = end_date
        self.quote = quote
        self.opinion = opinion
        self._book_id = book_id
        
    @property  
    def book_id(self):
        return self._book_id
    
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, title):
        self.validation_str(title)
        self._title = title.strip().title()
        
    @property 
    def author(self):
        return self._author
    @author.setter
    def author(self, author):
        self.validation_str(author)
        self._author = author.strip().title()
        
        
    @property
    def genre(self):
        return self._genre
    @genre.setter
    def genre(self, genre):
        self.validation_str(genre)
        self._genre = genre.strip()
        
        
    @property
    def start_date(self):
        return self._start_date
    @start_date.setter
    def start_date(self, start_date):
        self.validation_date(start_date)
        if hasattr(self, "_end_date") and self._end_date is not None:
                self.validation_end_date(start_date, self._end_date)
        self._start_date = start_date
        
    @property
    def end_date(self):
        return self._end_date
    @end_date.setter
    def end_date(self, end_date):
        if end_date is not None:
            self.validation_date(end_date)
            self.validation_end_date(self.start_date, end_date)
        self._end_date = end_date
        
        
    @property
    def quote(self):
        return self._quote
    @quote.setter
    def quote(self, quote):
        quote = self.validation_optional_text(quote)
        self._quote = quote
        
    @property
    def opinion(self):
        return self._opinion
    @opinion.setter
    def opinion(self, opinion):
        opinion = self.validation_optional_text(opinion)
        self._opinion = opinion
               
    
    def __str__(self):
        return f"Book: {self.title}\nAuthor: {self.author}\nGenre: {self.genre}"
    
    @staticmethod
    def validation_str(string):
        if isinstance(string, str):
            if not string.strip():
                raise ValueError("String cannot be empty")
        else:
            raise TypeError("Value must be a string")
        
    @staticmethod
    def validation_optional_text(string):
        if string is not None:
            if isinstance(string, str):
                if not string.strip():
                    return None
                else:
                    return string.strip()
            else:
                raise TypeError("Value must be a string")
        else:
            return None
            
    @staticmethod
    def validation_date(value):
        if type(value) is not date:
            raise TypeError("Date must be a date object")
    @staticmethod   
    def validation_end_date(start, end):
        if start > end:
            raise ValueError("End date can't be before start date")
    
    
    def is_finished(self):
        return self.end_date is not None
    
    def days_to_read(self):
        if self.end_date is not None:
            day = (self.end_date - self.start_date).days + 1
            return day
        else:
            return None
    