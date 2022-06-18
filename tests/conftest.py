import pytest
import mongomock
from project import create_app
import project.database

@pytest.fixture(autouse=True)
def test_client(monkeypatch):
    app = create_app()
    app.config['TESTING'] = True

    mongo_mock = mongomock.MongoClient()
    monkeypatch.setattr(project.database, 'mongo', mongo_mock)

    # login is tested based on this credentials
    mongo_mock.db.users.insert_one({ "username": "username", "password": "password" })

    yield app.test_client()