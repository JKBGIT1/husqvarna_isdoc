import settings
from pymongo.mongo_client import MongoClient

def init_db():
    client = MongoClient(
        settings.MONGO_URL,
        int(settings.MONGO_PORT),
        username=settings.MONGO_USERNAME,
        password=settings.MONGO_PASSWORD
    )

    db = client.flask_db

    return db