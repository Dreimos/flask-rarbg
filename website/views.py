from __future__ import annotations
from flask.views import MethodView
from flask import render_template, abort, request

import requests
import re

from . import db
from website.models import UploadData, Categories
from website.config import OMDB_API_KEY

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from flask_sqlalchemy.pagination import Pagination
    from flask_sqlalchemy.query import Query

class CategoryFetcher:
    def fetch_all_categories(self) -> list:
        return db.session.query(Categories).all()

class ListView(MethodView, CategoryFetcher):
    init_every_request = False
    items_per_page = 40

    def __init__(self, template: str) -> None:
        self.model = UploadData
        self.template = template

    def _get_query(self) -> Query:
        return db.session.query(self.model)

    def _get_paginated(self, query: Query, page: int, per_page: int) -> Pagination:
        return query.paginate(page=page, per_page=per_page)

    def _to_dict(self, item: UploadData) -> dict[str, str|int]:
        item_dict = {
                'id': item.id,
                'title': item.title,
                'category': item.cat,
                'size': item.size,
                }
        return item_dict
    
    def fetch_data(self, page: int) -> tuple[list[dict[str, str|int]], int]:
        output = self._get_paginated(self._get_query(), page, self.items_per_page)
        page_entries = [self._to_dict(item) for item in output]
        return page_entries, output.pages

    def get(self, page_num: int|None=None) -> str:
        category_list = self.fetch_all_categories()
        cur_page = page_num if page_num is not None else 1
        table_data, page_num = self.fetch_data(cur_page)
        return render_template(self.template, category_list=category_list, table_data=table_data, page=cur_page, page_num=page_num)


class CategoryListView(ListView):
    def _get_query(self) -> Query:
        return db.session.query(self.model).filter_by(cat=self.cat) 

    def _fetch_categories(self) -> list[str]:
        categories = db.session.query(Categories).all()
        output = [item.cat for item in categories]
        return(output)
    
    def get(self, cat:str|None=None, page_num: int|None=None) -> str:
        if cat is not None and cat in self._fetch_categories():
            self.cat = cat
        else:
            abort(404)
        return super().get(page_num)


class SearchListView(CategoryListView):
    def _breakdown_into_keywords(self, text: str|None) -> set[str]:
        if text is None:
            return set()
        separators = r'[,\s=;*\\]+'
        return {f"%{word}%" for word in re.split(separators, text)}
    
    def _get_query(self) -> Query:
        if self.cat is None:
            filtered = db.session.query(self.model)
        else:
            filtered = db.session.query(self.model).filter_by(cat=self.cat)
        for key in self.keywords:
            filtered = filtered.filter(self.model.title.like(key))
        return filtered
    
    def get(self, search_query:str|None=None, cat: str|None=None, page_num: int=1) -> str:
        search_query = request.args.get('search_query') if search_query is None else search_query
        self.keywords = self._breakdown_into_keywords(search_query)
        self.cat = cat
        return super(CategoryListView, self).get(page_num)

class DetailView(MethodView, CategoryFetcher):
    init_every_request = False

    def __init__(self) -> None:
        self.model = UploadData

    def _get_item(self, id: int) -> UploadData:
        return db.session.query(self.model).get_or_404(id)

    def _to_dict(self, item: UploadData) -> dict:
        item_dict = {
                    'id': item.id,
                    'hash': item.hash,
                    'title': item.title,
                    'category': item.cat,
                    'size': item.size,
                    'imdb': item.imdb,
                    }
        return item_dict

    def _fetch_imdb(self, imdb_id: str, api_key: str|None) -> dict[str, Any]|None:
        """
        Fetches the imdb data based on an id using OMDB as the API provider.
        """
        if api_key is None:
            return None
        url = "http://www.omdbapi.com/"
        params = {
                'i': imdb_id,
                'plot': 'full',
                'apikey': api_key,
                }
        try:
            response = requests.get(url=url, params=params)
            output = response.json()
        except requests.exceptions.RequestException:
            return None
        else:
            return output


    def get(self, id: int) -> str:
        category_list = self.fetch_all_categories()
        item = self._get_item(id)
        table_data = self._to_dict(item)
        if table_data['imdb'] is not None:
            imdb_data = self._fetch_imdb(table_data['imdb'], OMDB_API_KEY)
        else:
            imdb_data = None
        return render_template("detail.html", category_list=category_list, table_data=table_data, imdb_data=imdb_data)

