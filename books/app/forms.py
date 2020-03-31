from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

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

class BookReviewForm(FlaskForm):
    rating = DecimalField('Rating', places=2,validators=[NumberRange(min=0, max=5),DataRequired()])
    review_text = TextAreaField('Review', validators=[DataRequired()])
    submit = SubmitField('Submit')