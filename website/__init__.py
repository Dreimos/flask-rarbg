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

    from .views import ListView, DetailView, CategoryListView, SearchListView
    
    # TODO: set up url paths
    app.add_url_rule("/", view_func=ListView.as_view('home', template="list_view.html"))
    app.add_url_rule("/<int:page_num>/", view_func=ListView.as_view('list_view', template="list_view.html"))
    app.add_url_rule("/category/<string:cat>/<int:page_num>/", view_func=CategoryListView.as_view('category_list', template="category_list_view.html"))
    app.add_url_rule("/detail/<int:id>/", view_func=DetailView.as_view('upload_detail'))
    app.add_url_rule("/search/", view_func=SearchListView.as_view('search_list', template="search_view.html"))
    app.add_url_rule("/search/<string:search_query>/<int:page_num>", view_func=SearchListView.as_view('search_paginated', template="search_view.html"))

    return app

