import os
from flask import Flask
from project.site.site import site

def create_app():
    # create and configure the app
    app = Flask(__name__)

    SECRET_KEY = str(os.getenv('HUSQVARNA_APP_SECRET_KEY') or 'secret')
    app.config['SECRET_KEY'] = SECRET_KEY

    app.register_blueprint(site)
    
    return app