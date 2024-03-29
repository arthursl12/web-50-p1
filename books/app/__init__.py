import os
import requests

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import LoginManager

from app.config import Config


app = Flask(__name__)
app.config.from_object(Config)

# Session(app)
engine = create_engine(os.getenv("DATABASE_URL"), pool_recycle=3600) # database engine object from SQLAlchemy that manages connections to the database
                                                    # DATABASE_URL is an environment variable that indicates where the database lives
db = scoped_session(sessionmaker(bind=engine))

from app import auth
app.register_blueprint(auth.bp)

from app import routes

app.run(debug=True)