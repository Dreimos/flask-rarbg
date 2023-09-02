from flask.views import MethodView
from flask import render_template, abort, request, redirect, url_for
from sqlalchemy import text, func

import requests
import re

from . import db
from .models import UploadData, Categories
from .config import OMDB_API_KEY

class ListView(MethodView):
    init_every_request = False
    items_per_page = 40

    def __init__(self, template):
        self.model = UploadData
        self.template = template

    def _get_query(self):
        return db.session.query(self.model)

    def _get_paginated(self, query, page, per_page):
        return query.paginate(page=page, per_page=per_page)

    def _to_dict(self, item):
        item_dict = {
                'id': item.id,
                'title': item.title,
                'category': item.cat,
                'size': item.size,
                }
        return item_dict
    
    def fetch_data(self, page):
        output = self._get_paginated(self._get_query(), page, self.items_per_page)
        page_entries = [self._to_dict(item) for item in output]
        return page_entries, output.pages

    def get(self, page_num=None):
        cur_page = page_num if page_num is not None else 1
        table_data, page_num = self.fetch_data(cur_page)
        return render_template(self.template, table_data=table_data, page=cur_page, page_num=page_num)


class CategoryListView(ListView):
    def _get_query(self):
        return db.session.query(self.model).filter_by(cat=self.cat) 

    def _fetch_categories(self):
        categories = db.session.query(Categories).all()
        output = [item.cat for item in categories]
        return(output)
    
    def get(self, cat=None, page_num=None):
        if cat is not None and cat in self._fetch_categories():
            self.cat = cat
        else:
            abort(404)
        return super().get(page_num)


class SearchListView(CategoryListView):
    def _breakdown_into_keywords(self, text):
        separators = r'[,\s=;*\\]+'
        return {f"%{word}%" for word in re.split(separators, text)}
    
    def _get_query(self):
        if self.cat is None:
            filtered = db.session.query(self.model)
        else:
            filtered = db.session.query(self.model).filter_by(cat=self.cat)
        for key in self.keywords:
            filtered = filtered.filter(self.model.title.like(key))
        return filtered
    
    def get(self, search_query=None, cat=None, page_num=1):
        search_query = request.args.get('search_query') if search_query is None else search_query
        self.keywords = self._breakdown_into_keywords(search_query)
        self.cat = cat
        return super(CategoryListView, self).get(page_num)

class DetailView(MethodView):
    init_every_request = False

    def __init__(self) -> None:
        self.model = UploadData

    def _get_item(self, id):
        return db.session.query(self.model).get_or_404(id)

    def _to_dict(self, item) -> dict:
        item_dict = {
                    'id': item.id,
                    'hash': item.hash,
                    'title': item.title,
                    'category': item.cat,
                    'size': item.size,
                    'imdb': item.imdb,
                    }
        return item_dict

    def _fetch_imdb(self, imdb_id):
        url = "http://www.omdbapi.com/"
        params = {
                'i': imdb_id,
                'plot': 'full',
                'apikey': OMDB_API_KEY,
                }
        try:
            r = requests.get(url=url, params=params)
            output = r.json()
        except requests.exceptions.RequestException:
            # TODO: proper handling of request exceptions
            pass
        else:
            return output


    def get(self, id):
        item = self._get_item(id)
        table_data = self._to_dict(item)
        if table_data['imdb'] is not None:
            imdb_data = self._fetch_imdb(table_data['imdb'])
        else:
            imdb_data = None
        return render_template("detail.html", table_data=table_data, imdb_data=imdb_data)

