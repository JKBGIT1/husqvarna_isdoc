import settings
from flask import Flask

def create_app():
    # create and configure the app
    app = Flask(__name__)

    app.config['SECRET_KEY'] = settings.SECRET_KEY

    from project.site import site
    app.register_blueprint(site)
    
    return app