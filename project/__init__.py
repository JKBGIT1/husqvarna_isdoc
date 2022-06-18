import settings
from flask import Flask

def create_app():
    # create and configure the app
    app = Flask(__name__)

    app.config['SECRET_KEY'] = settings.SECRET_KEY

    from project.login_manager import login_manager
    login_manager.init_app(app)

    from project.blueprints.site import site
    app.register_blueprint(site)
    
    return app