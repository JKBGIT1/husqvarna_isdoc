import pytest
from project.init import create_app

# source: https://testdriven.io/blog/flask-pytest/
@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client # execution is being passed to the test functions.