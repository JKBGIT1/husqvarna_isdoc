from flask import Flask
from project.site.site_blueprint import site

def create_app():
    # create and configure the app
    app = Flask(__name__)

    app.register_blueprint(site)
    
    return app