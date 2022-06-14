import settings
from flask import Flask
from pymongo.mongo_client import MongoClient
from project.site import site

def create_app():
    # create and configure the app
    app = Flask(__name__)

    app.config['SECRET_KEY'] = settings.SECRET_KEY

    app.register_blueprint(site)
    
    return app