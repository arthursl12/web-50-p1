import os


class Config(object):
    DATABASE_URL = os.getenv("DATABASE_URL") or "mysql+pymysql://root:@localhost:3306/p1db"
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET-KEY") or "you-really-will-never-guess"
    

