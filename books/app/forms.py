from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, ValidationError

from app import db
from app.users import checkPassword

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
    rating = StringField('Rating',validators=[DataRequired()])
    review_text = TextAreaField('Review', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_rating(self, rating):
        if (not rating.data.isnumeric()) and (not rating.data.replace('.','',1).isdigit()):
            raise ValidationError('Please insert a number between 0 and 5')
        rat = float(rating.data)
        if rat < 0 or rat > 5:
            raise ValidationError('Please insert a number between 0 and 5')
        rat_round = round(rat, 1)
        if rat_round != rat:
            raise ValidationError('Please insert a number with at most one decimal digit')