from bson.objectid import ObjectId
from flask_login import LoginManager
import project.database
from project.models import User

login_manager = LoginManager()
login_manager.login_view = 'site.login'  # type: ignore -> Bug referring to None
login_manager.login_message_category = 'info'
login_manager.login_message = 'Pre túto akciu je potrebné prihlásenie.'

@login_manager.user_loader
def load_user(id: str):
    user = project.database.mongo.db.users.find_one({ "_id": ObjectId(id) })

    if user:
        return User(id)

    return None