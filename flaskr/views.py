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


""" @bp.route('/grocery')
def grocery():
    #? check session
    return render_template('views/grocery.html') """

@bp.route('/household')
def household():
    #? check session
    return render_template('views/household.html')

@bp.route('/vehicle')
def vehicle():
    #? check session
    return render_template('views/vehicle.html')


