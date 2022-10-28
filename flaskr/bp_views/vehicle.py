# INF601 - Advanced Programming in Python
# James Kobell
# Mini Project 3

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.db import get_db

from werkzeug.exceptions import abort

from flaskr.auth import login_required

bp = Blueprint('vehicle', __name__, url_prefix='/views/vehicle')

@bp.route('/vehicle')
def vehicle():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, make_model, items_text, created, author_id, username'
        ' FROM vehicle p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    #? check session
    return render_template('/views/vehicle/vehicle.html', posts=posts, tablename = 'Vehicle')

@bp.route('/createvehicle', methods=('GET', 'POST'))
@login_required
def createvehicle():
    if request.method == 'POST':
        make_model = request.form['make_model']
        items_text = request.form['items_text']
        error = None

        if not make_model:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO vehicle (make_model, items_text, author_id)'
                ' VALUES (?, ?, ?)',
                (make_model, items_text, g.user['id'])
            )
            db.commit()
            return redirect(url_for('vehicle.vehicle'))

    return render_template('views/vehicle/createvehicle.html')

def get_postvehicle(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, make_model, items_text, created, author_id, username'
        ' FROM vehicle p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/updatevehicle', methods=('GET', 'POST'))
@login_required
def updatevehicle(id):
    post = get_postvehicle(id)

    if request.method == 'POST':
        make_model = request.form['make_model']
        items_text = request.form['items_text']
        error = None

        if not make_model:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE vehicle SET make_model = ?, items_text = ?'
                ' WHERE id = ?',
                (make_model, items_text, id)
            )
            db.commit()
            return redirect(url_for('vehicle.vehicle'))

    return render_template('views/vehicle/updatevehicle.html', post=post)

@bp.route('/<int:id>/deletevehicle', methods=('POST',))
@login_required
def deletevehicle(id):
    get_postvehicle(id)
    db = get_db()
    db.execute('DELETE FROM vehicle WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('vehicle.vehicle'))