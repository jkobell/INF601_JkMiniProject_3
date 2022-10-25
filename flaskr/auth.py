# INF601 - Advanced Programming in Python
# James Kobell
# Mini Project 3
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash #always hash passwords

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST')) #register function URL and options
def register(): # user registration
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",# sql to create user in table user
                    (username, generate_password_hash(password)), # password is hashed before persisting
                )
                db.commit()
            except db.IntegrityError: # todo: add logging
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login")) # sql INSERT successful, redirect to login view 

        flash(error)

    return render_template('auth/register.html')# return html to browser

@bp.route('/login', methods=('GET', 'POST'))#register function URL and options
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id'] # set session with user id
            return redirect(url_for('views.index')) # redirect to views index

        flash(error)

    return render_template('auth/login.html') # redirect to login view if login fails

@bp.before_app_request
def load_logged_in_user(): # check if session user id exists in db user table each view request
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login')) # redirect to login view after logout

def login_required(view): # verify if session is valid
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view