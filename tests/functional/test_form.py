def test_login_form(test_client):
    response = test_client.get('/')
    assert response.status_code == 200

    page_content = response.text

    labels = ['Používateľské meno', 'Heslo']
    for label in labels:
        assert label in page_content

def test_sunny_day_submit(test_client):
    data = {
        "username": "username",
        "password": "password"
    }

    response = test_client.post('/', data=data, follow_redirects=True)

    assert len(response.history) == 1 # there has to be one redirect
    assert response.status_code == 200
    assert response.request.path == '/home'

def test_not_filled_user_data(test_client):
    data = {
        "username": "",
        "password": ""
    }

    response = test_client.post('/', data=data)

    assert response.status_code == 400
    assert 'Vyplnte prihlásovacia údaje.' in response.text

def test_not_filled_username(test_client):
    data = {
        "username": "",
        "password": "password"
    }

    response = test_client.post('/', data=data)

    assert response.status_code == 400
    assert 'Vyplnte prihlásovacia údaje.' in response.text

def test_not_filled_password(test_client):
    data = {
        "username": "username",
        "password": ""
    }

    response = test_client.post('/', data=data)

    assert response.status_code == 400
    assert 'Vyplnte prihlásovacia údaje.' in response.text