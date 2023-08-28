from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import SECRET_KEY, SQLALCHEMY_DATABASE_URI

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    db.init_app(app)
    app.app_context().push()

    from .views import ListView

    app.add_url_rule("/", view_func=ListView.as_view('list_view'))

    return app

def create_db(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context(): 
            db.create_all()
