import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine(os.getenv("DATABASE_URL"), pool_recycle=3600) # database engine object from SQLAlchemy that manages connections to the database
                                                    # DATABASE_URL is an environment variable that indicates where the database lives
db = scoped_session(sessionmaker(bind=engine))

def findUser(_id):
    user = db.execute("SELECT * FROM user WHERE id = :id",
                        {"id": _id}).fetchone()
    db.close() 
    if user == None: raise Exception('usuário com esse ID não existe')
    return user

def createUser(_name, _login, _password):
    db.execute("INSERT INTO user (name, login, hash) VALUES (:name, :login, :hash)",
            {"name": _name, 
            "login": _login,
            "hash": generate_password_hash(_password)})
    print(f"User criado:{_name}, {_login}")
    db.commit()
    db.close() 
    

def checkPassword(login, password):
    user = db.execute("SELECT * FROM user WHERE login = :login",
                        {"login": login}).fetchone()
    db.close() 
    return check_password_hash(user.hash, password)