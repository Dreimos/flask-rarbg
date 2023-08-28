from flask.views import View
from . import db
from .models import UploadData

class ListView(View):
    methods = ['GET']

    def dispatch_request(self):
        val = db.session.query(UploadData).first()
        print(val.hash)
        return ""
