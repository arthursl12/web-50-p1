from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


def find_user(_id):
    user = db.execute("SELECT * FROM user WHERE id = :id",
                        {"id": _id}).fetchone()
    
    if user == None: raise Exception('usuário com esse ID não existe')
    return user

def create_user(_name, _login, _password):
    db.execute("INSERT INTO user (name, login, hash) VALUES (:name, :login, :hash)",
            {"name": _name, 
            "login": _login,
            "hash": generate_password_hash(_password)})
    print(f"User criado:{_name}, {_login}")
    db.commit()


def set_password(password):
    self.password_hash = generate_password_hash(password)

def check_password(login, password):
    user = db.execute("SELECT * FROM user WHERE login = :login",
                        {"login": login}).fetchone()
    return check_password_hash(user.hash, password)