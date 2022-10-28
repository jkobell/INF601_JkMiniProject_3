# INF601 - Advanced Programming in Python
# James Kobell
# Mini Project 3

from flask import (
    Blueprint, render_template
)

bp = Blueprint('views', __name__, url_prefix='/views')

@bp.route('/index')
def index():
    #? check session
    return render_template('views/index.html')
