from flask.views import View, MethodView
from flask import render_template

import requests

from . import db
from .models import UploadData
from .config import OMDB_API_KEY

class ListView(View):
    methods = ['GET']

    def dispatch_request(self):
        return ""

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
