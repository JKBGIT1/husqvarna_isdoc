import pytest
import mongomock
from project import create_app
import project.db


@pytest.fixture(autouse=True)
def test_client(monkeypatch):
    app = create_app()
    app.config['TESTING'] = True

    mongo_mock = mongomock.MongoClient()
    monkeypatch.setattr(project.db, 'mongo', mongo_mock)

    # login is tested based on this credentials
    project.db.mongo.db.users.insert_one({ "username": "username", "password": "password" })

    yield app.test_client()