# INF601 - Advanced Programming in Python
# James Kobell
# Mini Project 3
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

from werkzeug.exceptions import abort

from flaskr.auth import login_required

bp = Blueprint('grocery', __name__, url_prefix='/views/grocery')

@bp.route('/grocery')
def grocery():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, category, items_text, created, author_id, username'
        ' FROM grocery p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    #? check session
    return render_template('/views/grocery/grocery.html', posts=posts, tablename = 'Grocery')

@bp.route('/creategrocery', methods=('GET', 'POST'))
@login_required
def creategrocery():
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
                'INSERT INTO grocery (category, items_text, author_id)'
                ' VALUES (?, ?, ?)',
                (category, items_text, g.user['id'])
            )
            db.commit()
            return redirect(url_for('grocery.grocery'))

    return render_template('views/grocery/creategrocery.html')

def get_postgrocery(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, category, items_text, created, author_id, username'
        ' FROM grocery p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/updategrocery', methods=('GET', 'POST'))
@login_required
def updategrocery(id):
    post = get_postgrocery(id)

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
                'UPDATE grocery SET category = ?, items_text = ?'
                ' WHERE id = ?',
                (category, items_text, id)
            )
            db.commit()
            return redirect(url_for('grocery.grocery'))

    return render_template('views/grocery/updategrocery.html', post=post)

@bp.route('/<int:id>/deletegrocery', methods=('POST',))
@login_required
def deletegrocery(id):
    get_postgrocery(id)
    db = get_db()
    db.execute('DELETE FROM grocery WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('grocery.grocery'))