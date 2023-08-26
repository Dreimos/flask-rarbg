from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from os import path, getenv

DEBUG = True

DB_NAME = 'rarbg_db.sqlite'
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_NAME}"
SECRET_KEY = getenv('SECRET_KEY', '56qHPqfU6Azk@R@eEfja7JzpdiyxTBvYJwFzRk3wRY$2sQ&3oFaC')

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    db.init_app(app)
    
    from .views import ListView

    app.add_url_rule("/", view_func=ListView.as_view('list_view'))

    return app

def create_db(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
