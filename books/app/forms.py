from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class BookSearchForm(FlaskForm):
    choices = [('title','Book Title'),
               ('author','Author'),
               ('isbn','ISBN')]
    select = SelectField('Search for books:', choices=choices)
    search = StringField('')