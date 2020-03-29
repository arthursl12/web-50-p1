import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.getenv("DATABASE_URL")) # database engine object from SQLAlchemy that manages connections to the database
                                                    # DATABASE_URL is an environment variable that indicates where the database lives
db = scoped_session(sessionmaker(bind=engine))

def importBooks():
    reader = csv.reader(open("books.csv"))
    db.execute("CREATE TABLE IF NOT EXISTS book(isbn VARCHAR(10) PRIMARY KEY, title VARCHAR(100), author VARCHAR(100), year YEAR);")
    for isbn,title,author,year in reader: # loop gives each column a name
        db.execute("INSERT INTO book (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                {"isbn": isbn, "title": title, "author": author, "year": year}) # substitute values from CSV line into SQL command, as per this dict
        print(f"Book:{isbn}, {title} from {author}, {year}")
    db.commit()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view