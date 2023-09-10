from os import getenv
from typing import Final

DEBUG: Final = True

DB_NAME: Final = 'rarbg_db.sqlite'
SQLALCHEMY_DATABASE_URI: Final = f"sqlite:///{DB_NAME}"
SECRET_KEY: Final = getenv('SECRET_KEY', '56qHPqfU6Azk@R@eEfja7JzpdiyxTBvYJwFzRk3wRY$2sQ&3oFaC')

# API key for external service used to retrieve IMDB data
# http://www.omdbapi.com/
OMDB_API_KEY:Final = getenv('OMDB_API_KEY')
