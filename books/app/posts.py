from app import db
from app.users import findUser

def addPost(user_id, book_isbn, rating, content):
    # Checking if the user and the book are valid
    findUser(user_id)
    book = db.execute("SELECT * FROM book WHERE isbn=:isbn",
                {"isbn": book_isbn}).fetchone()
    db.close()
    if book is None: 
        raise Exception("Livro não encontrado")
    

    # Add the post
    db.execute("INSERT INTO post (user_id, book_isbn, rating, post_content) VALUES (:id, :isbn, :rating, :content)",
                {"id": user_id, "isbn": book_isbn, "rating": rating, "content": content}) # substitute values from CSV line into SQL command, as per this dict
    print(f"Post from:{user_id} about {book_isbn} with rating {rating} added")
    db.commit()
    db.close() 

def getPosts(book_isbn):
    book = db.execute("SELECT * FROM book WHERE isbn=:isbn",
                {"isbn": book_isbn}).fetchone()
    db.close()
    if book is None: 
        raise Exception("Livro não encontrado")
    
    posts = db.execute("SELECT * FROM post WHERE book_isbn=:isbn",
                        {"isbn": book_isbn}).fetchall()
    db.close()
    return posts

def canPost(book_isbn, user_id):
    # Checking if the user and the book are valid
    findUser(user_id)
    book = db.execute("SELECT * FROM book WHERE isbn=:isbn",
                {"isbn": book_isbn}).fetchone()
    db.close()
    if book is None: 
        raise Exception("Livro não encontrado")
    
    # Checking if already posted
    posts = db.execute("SELECT * FROM post WHERE book_isbn=:isbn AND user_id=:id",
                        {"isbn": book_isbn, "id":user_id}).fetchone()
    db.close()
    if posts is None:
        return True
    else:
        return False

def howManyPosts(book_isbn):
    result = db.execute("SELECT COUNT(*) FROM post WHERE book_isbn=:isbn GROUP BY book_isbn",
                {"isbn": book_isbn}).fetchone()
    db.close()
    print(result)

    return result
