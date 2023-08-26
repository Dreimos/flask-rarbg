from flask.views import View
from . import db

class ListView(View):
    methods = ['GET']

    def dispatch_request(self):
        return super().dispatch_request()


