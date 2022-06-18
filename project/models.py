from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id: str) -> None:
        super().__init__()
        self.id = id

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False