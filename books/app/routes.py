from flask import Blueprint,render_template,session, flash, redirect, url_for, request, abort, g
import requests
import functools

from app.auth import login_required
from app import app
from app import db
from app.forms import LoginForm, BookSearchForm, BookReviewForm, RegisterForm
from app.users import checkPassword, findUser, createUser
from app.posts import addPost, getPosts, canPost

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
@app.route('/login/<alert>', methods=['GET', 'POST'])
def login(alert=""):
    form = LoginForm(request.form)
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
            flash('Login requested for user {}'.format(form.username.data))
            return redirect(url_for('search'))
    print(alert)
    if alert=="success": msg = "User created successfully! Please log in now."
    else: msg = ""

    return render_template('login.html', title='Sign In', form=form, alert=msg)

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
@app.route('/book/<isbn>/<alert>')
def bookPage(isbn, alert=""):
    book = db.execute("SELECT * FROM book WHERE isbn=:isbn", {"isbn": isbn}).fetchone()
    db.close() 
    # print(book)

    if g.user is None: user = None
    else: user = findUser(session['user_id'])

    if g.user is None: canpost = False
    else: canpost = canPost(isbn, session['user_id'])

    if alert == "success": msg = "Post added successfully!"
    else: msg = ""

    if book is None:
        abort(404)
    else:
        # Request from Goodreads API
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": GOODREADS_KEY, "isbns": isbn})
        book_json = (res.json())["books"][0]
        # print(book_json)

        # Render template
        # print(f"Book:{book.isbn}, {book.title} from {book.author}, {book.year}")
        print(canpost)
        return render_template('book.html', book=book, book_json=book_json, 
                                user=user, alert=msg, reviews=getPosts(isbn), canPost=canpost)


@app.route('/book/<isbn>/review', methods=['GET','POST'])
@login_required
def review(isbn):
    book = db.execute("SELECT * FROM book WHERE isbn=:isbn", {"isbn": isbn}).fetchone()
    db.close()

    reviewForm = BookReviewForm(request.form)
    if request.method == 'POST' and reviewForm.validate_on_submit():
        # The validation is actually held in the form class!
        addPost(session['user_id'], isbn, float(reviewForm.rating.data), reviewForm.review_text.data)
        return redirect(url_for('bookPage', isbn=isbn, alert="success"))
    return render_template('review.html', book=book, form=reviewForm, user=findUser(session['user_id']))

@app.route('/register', methods=['GET','POST'])
def register():
    registerForm = RegisterForm(request.form)

    if request.method == 'POST' and registerForm.validate_on_submit():
        # The validation is actually held in the form class
        print(registerForm.username.data)
        createUser(registerForm.username.data, registerForm.password.data)
        return redirect(url_for('login', alert="success"))
    return render_template('register.html', form=registerForm)


