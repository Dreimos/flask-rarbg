from sqlalchemy.ext.automap import automap_base
from . import db

Base = automap_base()
Base.prepare(autoload_with=db.engine)


"""
Relevant columns:
id - Primary Key
hash - magnet link UNIQUE
title - torrent name
cat - categories
size - upload size in bytes
imdb - imdb page (Nullable)
"""
# development table
UploadData = Base.classes.test_table
# main table
# UploadData = Base.classes.upload_data

