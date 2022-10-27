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

bp = Blueprint('views', __name__, url_prefix='/views')

@bp.route('/index')
def index():
    #? check session
    return render_template('views/index.html')

@bp.route('/buildingsupply')
def buildingsupply():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, project, items_text, created, author_id, username'
        ' FROM building_supply p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    #? check session
    return render_template('views/buildingsupply.html', posts=posts, tablename = 'BUILDING SUPPLY')

@bp.route('/createbuildingsupply', methods=('GET', 'POST'))
@login_required
def createbuildingsupply():
    if request.method == 'POST':
        project = request.form['project']
        items_text = request.form['items_text']
        error = None

        if not project:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO building_supply (project, items_text, author_id)'
                ' VALUES (?, ?, ?)',
                (project, items_text, g.user['id'])
            )
            db.commit()
            return redirect(url_for('views.buildingsupply'))

    return render_template('views/createbuildingsupply.html')

def get_postbuildingsupply(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, project, items_text, created, author_id, username'
        ' FROM building_supply p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/updatebuildingsupply', methods=('GET', 'POST'))
@login_required
def updatebuildingsupply(id):
    post = get_postbuildingsupply(id)

    if request.method == 'POST':
        project = request.form['project']
        items_text = request.form['items_text']
        error = None

        if not project:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE building_supply SET project = ?, items_text = ?'
                ' WHERE id = ?',
                (project, items_text, id)
            )
            db.commit()
            return redirect(url_for('views.buildingsupply'))

    return render_template('views/updatebuildingsupply.html', post=post)

@bp.route('/<int:id>/deletebuildingsupply', methods=('POST',))
@login_required
def deletebuildingsupply(id):
    get_postbuildingsupply(id)
    db = get_db()
    db.execute('DELETE FROM building_supply WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('views.buildingsupply'))

@bp.route('/grocery')
def grocery():
    #? check session
    return render_template('views/grocery.html')

@bp.route('/household')
def household():
    #? check session
    return render_template('views/household.html')

@bp.route('/vehicle')
def vehicle():
    #? check session
    return render_template('views/vehicle.html')


