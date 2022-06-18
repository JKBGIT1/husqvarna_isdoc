import settings
from pymongo.mongo_client import MongoClient

mongo = MongoClient(
    settings.MONGO_URL,
    int(settings.MONGO_PORT),
    username=settings.MONGO_USERNAME,
    password=settings.MONGO_PASSWORD
)