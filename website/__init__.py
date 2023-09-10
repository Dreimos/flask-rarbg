from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy import text

from website.config import SECRET_KEY, SQLALCHEMY_DATABASE_URI

db = SQLAlchemy()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    db.init_app(app)
    alter_table(app)
    app.app_context().push()

    from website.views import ListView, DetailView, CategoryListView, SearchListView

    app.add_url_rule("/", view_func=ListView.as_view('home', template="list_view.html"))
    app.add_url_rule("/<int:page_num>/", view_func=ListView.as_view('list_view', template="list_view.html"))
    app.add_url_rule("/category/<string:cat>/<int:page_num>/", view_func=CategoryListView.as_view('category_list', template="category_list_view.html"))
    app.add_url_rule("/detail/<int:id>/", view_func=DetailView.as_view('upload_detail'))
    app.add_url_rule("/search/", view_func=SearchListView.as_view('search_list', template="search_view.html"))
    app.add_url_rule("/search/<string:search_query>/<int:page_num>", view_func=SearchListView.as_view('search_paginated', template="search_view.html"))

    return app

def alter_table(app: Flask) -> None:
    """
    Checks input database and renames it if the name is incompatible.
    Afterwards checks if there is a category table and creates one if none is found.
    """
    with app.app_context():
        # The original 'items' name of the table conflicts with SQLAlchemy, so I renamed it.
        if Inspector.from_engine(db.engine).has_table('items'):
            db.session.execute(text("ALTER TABLE items RENAME TO upload_data"))
        # The database is not normalized, so for some functionality I had to create a categories table
        if not Inspector.from_engine(db.engine).has_table('categories'):
            db.session.execute(text("CREATE TABLE categories (cat TEXT UNIQUE, PRIMARY KEY (cat))"))
            db.session.execute(text("INSERT INTO categories SELECT DISTINCT cat FROM upload_data"))
            db.session.commit()
