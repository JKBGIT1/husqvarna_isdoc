from bson.objectid import ObjectId
from flask_login import LoginManager
from project.database import mongo
from project.models import User

login_manager = LoginManager()
login_manager.login_view = 'site.login'  # type: ignore -> Bug referring to None
login_manager.login_message_category = 'info'
login_manager.login_message = 'Pre túto akciu je potrebné prihlásenie.'

@login_manager.user_loader
def load_user(id: str):
    user = mongo.db.users.find_one({ "_id": ObjectId(id) })

    if user:
        return User(id)

    return None