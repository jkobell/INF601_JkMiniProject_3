# INF601 - Advanced Programming in Python
# James Kobell
# Mini Project 3

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.db import get_db

from werkzeug.exceptions import abort

from flaskr.auth import login_required

#create blueprint object with parameters
bp = Blueprint('home', __name__, url_prefix='/views/home')
# read view rendered from db SELECT results
@bp.route('/home')
def home():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, category, items_text, created, author_id, username'
        ' FROM home p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('/views/home/home.html', posts=posts, tablename = 'HOUSEHOLD')
# create view - INSERT to db
@bp.route('/createhome', methods=('GET', 'POST'))
@login_required
def createhome():
    if request.method == 'POST':
        category = request.form['category']
        items_text = request.form['items_text']
        error = None

        if not category:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO home (category, items_text, author_id)'
                ' VALUES (?, ?, ?)',
                (category, items_text, g.user['id'])
            )
            db.commit()
            return redirect(url_for('home.home'))

    return render_template('views/home/createhome.html')
# SELECT only 1 record from db for edit or delete
def get_posthome(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, category, items_text, created, author_id, username'
        ' FROM home p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post
# UPDATE single record
@bp.route('/<int:id>/updatehome', methods=('GET', 'POST'))
@login_required # check if user is logged in
def updatehome(id):
    post = get_posthome(id)

    if request.method == 'POST':
        category = request.form['category']
        items_text = request.form['items_text']
        error = None

        if not category:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE home SET category = ?, items_text = ?'
                ' WHERE id = ?',
                (category, items_text, id)
            )
            db.commit()
            return redirect(url_for('home.home'))

    return render_template('views/home/updatehome.html', post=post)
# DELETE single record from db
@bp.route('/<int:id>/deletehome', methods=('POST',))
@login_required
def deletehome(id):
    get_posthome(id)
    db = get_db()
    db.execute('DELETE FROM home WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('home.home'))