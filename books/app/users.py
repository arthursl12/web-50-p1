from werkzeug.security import generate_password_hash, check_password_hash
from app import db

def findUser(_id):
    user = db.execute("SELECT * FROM user WHERE id = :id",
                        {"id": _id}).fetchone()
    db.close() 
    if user == None: raise Exception('usuário com esse ID não existe')
    return user

def createUser(_login, _password):
    db.execute("INSERT INTO user (login, hash) VALUES (:login, :hash)",
            {"login": _login,
            "hash": generate_password_hash(_password)})
    print(f"User criado {_login}")
    db.commit()
    db.close() 
    

def checkPassword(login, password):
    user = db.execute("SELECT * FROM user WHERE login = :login",
                        {"login": login}).fetchone()
    db.close() 
    return check_password_hash(user.hash, password)