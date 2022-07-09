import pytest
import mongomock
from project import create_app
import project.database

@pytest.fixture(autouse=True)
def test_client(monkeypatch):
    app = create_app()
    app.config['TESTING'] = True

    # this allows using url_for in tests
    context = app.test_request_context()
    context.push()

    mongo_mock = mongomock.MongoClient()
    monkeypatch.setattr(project.database, 'mongo', mongo_mock)

    # login is tested based on this credentials
    mongo_mock.db.users.insert_one({ "username": "username", "password": "password" })

    yield app.test_client()