from flask import Blueprint

site = Blueprint('site_blueprint', __name__)

@site.route('/')
def index():
    return "<h2>Hello World!</h2>"