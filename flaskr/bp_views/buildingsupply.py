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
bp = Blueprint('buildingsupply', __name__, url_prefix='/views/buildingsupply')
# read view rendered from db SELECT results
@bp.route('/buildingsupply')
def buildingsupply():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, project, items_text, created, author_id, username'
        ' FROM building_supply p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('/views/buildingsupply/buildingsupply.html', posts=posts, tablename = 'BUILDING SUPPLY')
# create view - INSERT to db
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
            return redirect(url_for('buildingsupply.buildingsupply'))

    return render_template('views/buildingsupply/createbuildingsupply.html')
# SELECT only 1 record from db for edit or delete
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
# UPDATE single record
@bp.route('/<int:id>/updatebuildingsupply', methods=('GET', 'POST'))
@login_required # check if user is logged in
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
            return redirect(url_for('buildingsupply.buildingsupply'))

    return render_template('views/buildingsupply/updatebuildingsupply.html', post=post)
# DELETE single record from db
@bp.route('/<int:id>/deletebuildingsupply', methods=('POST',))
@login_required
def deletebuildingsupply(id):
    get_postbuildingsupply(id)
    db = get_db()
    db.execute('DELETE FROM building_supply WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('buildingsupply.buildingsupply'))
