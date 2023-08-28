from os import getenv

DEBUG = True

DB_NAME = 'rarbg_db.sqlite'
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_NAME}"
SECRET_KEY = getenv('SECRET_KEY', '56qHPqfU6Azk@R@eEfja7JzpdiyxTBvYJwFzRk3wRY$2sQ&3oFaC')
