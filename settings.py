import os

FLASK_PORT = int(os.getenv('PORT') or '5000')
DEV = bool(os.getenv('DEV') or True)
SECRET_KEY = str(os.getenv('HUSQVARNA_APP_SECRET_KEY') or 'secret')
URL_PREFIX = str(os.getenv('URL_PREFIX') or '/husqvarna_isdoc')

MONGO_URL = str(os.getenv('MONGO_URL') or 'localhost')
MONGO_PORT = str(os.getenv('MONGO_PORT') or 27017)
MONGO_USERNAME = str(os.getenv('MONGO_INITDB_ROOT_USERNAME') or 'root')
MONGO_PASSWORD = str(os.getenv('MONGO_INITDB_ROOT_PASSWORD') or 'password')