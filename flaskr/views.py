# INF601 - Advanced Programming in Python
# James Kobell
# Mini Project 3
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('views', __name__, url_prefix='/views')

@bp.route('/index')
def index():
    #? check session
    return render_template('views/index.html')
