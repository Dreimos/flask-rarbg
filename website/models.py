from sqlalchemy.ext.automap import automap_base

from . import db

Base = automap_base()

class UploadData(Base):
    """
    Relevant columns:
    id - Primary Key
    hash - magnet link UNIQUE
    title - torrent name
    cat - categories
    size - upload size in bytes
    imdb - imdb page (Nullable)
    """
    __tablename__ = 'upload_data'

class Categories(Base):
    __tablename__ = 'categories'

Base.prepare(autoload_with=db.engine)

