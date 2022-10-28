# INF601 - Advanced Programming in Python
# James Kobell
# Mini Project 3
import os

from flask import Flask

# app object is created from a Flask instance
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    # checks if run as a test then load test config; if not, load app config
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:        
        app.config.from_mapping(test_config)

    # check if SQLite folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    from . import db
    db.init_app(app)

    # register all blueprints *.py files
    from . import auth
    app.register_blueprint(auth.bp)

    from . import views
    app.register_blueprint(views.bp)

    from .bp_views import buildingsupply
    app.register_blueprint(buildingsupply.bp, url_prefix='/bp_views')

    from .bp_views import grocery
    app.register_blueprint(grocery.bp, url_prefix='/bp_views')

    from .bp_views import home
    app.register_blueprint(home.bp, url_prefix='/bp_views')

    from .bp_views import vehicle
    app.register_blueprint(vehicle.bp, url_prefix='/bp_views')

    return app