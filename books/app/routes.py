from flask import Blueprint,render_template,session, flash, redirect, url_for, request, abort, g
import requests
import functools

from app.auth import login_required
from app import app
from app import db
from app.forms import LoginForm, BookSearchForm, BookReviewForm
from app.users import checkPassword, findUser

GOODREADS_KEY = "qwAYxunHEt6KnQJzDskA"


@app.route("/")
@app.route('/index')
def index():
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    user = findUser(session['user_id'])
    search = BookSearchForm()
    if request.method == 'POST':
        return search_results(search)
    return render_template('search.html', 
        title='Home', user=user, form=search)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.execute("SELECT * FROM user WHERE login = :login",
                          {"login": form.username.data}).fetchone()
        db.close() 
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

@app.route('/results')
@login_required
def search_results(search):
    # TODO: adaptar essa função para o SQLAlchemy puro
    # Função original de http://www.blog.pythonlibrary.org/2017/12/13/flask-101-how-to-add-a-search-form/
    results = []
    search_string = search.data['search']
    if search.data['search'] == '':
        qry = db_session.query(Album)
        results = qry.all()
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', results=results)
    
@app.route('/book/<isbn>')
def bookPage(isbn):
    book = db.execute("SELECT * FROM book WHERE isbn=:isbn", {"isbn": isbn}).fetchone()
    db.close() 
    # print(book)

    if g.user is None:
            user = None
    else:
        user = findUser(session['user_id'])



    if book is None:
        abort(404)
    else:
        # Request from Goodreads API
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": GOODREADS_KEY, "isbns": isbn})
        book_json = (res.json())["books"][0]
        # print(book_json)

        # Render template
        # print(f"Book:{book.isbn}, {book.title} from {book.author}, {book.year}")
    
        return render_template('book.html', book=book, book_json=book_json, user=user)

@app.route('/book/<isbn>/review', methods=['GET','POST'])
@login_required
def review(isbn):
    reviewForm = BookReviewForm()
    if reviewForm.validate_on_submit():
        pass
    return render_template('review.html', form=reviewForm, user=findUser(session['user_id']))
