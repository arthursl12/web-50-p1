from flask import render_template,session, flash, redirect, url_for

from app import app
from app import db
from app.forms import LoginForm
from app.users import checkPassword, findUser


@app.route("/")
@app.route('/index')
def index():
    return redirect(url_for('login'))

@app.route('/search')
def search():
    user = findUser(session['user_id'])
    return render_template('search.html', title='Home', user=user, userlogged=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.execute("SELECT * FROM user WHERE login = :login",
                          {"login": form.username.data}).fetchone()
        if user is None or not checkPassword(form.username.data, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        else:
            session.clear()
            session['user_id'] = user.id
            flash('Login requested for user {}'.format(
            form.username.data))
            return redirect(url_for('search'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))