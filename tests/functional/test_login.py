import re
from flask import url_for

def test_login_form(test_client):
    response = test_client.get(url_for('site.login'))
    assert response.status_code == 200

    page_content = response.text

    labels = ['Používateľské meno', 'Heslo']
    for label in labels:
        assert label in page_content

def test_sunny_day_login(test_client):
    data = {
        'username': 'username',
        'password': 'password'
    }

    response = test_client.post(url_for('site.login'), data=data, follow_redirects=True)

    assert len(response.history) == 1 # there has to be one redirect
    assert response.status_code == 200
    assert '/home' in response.request.path
    assert re.search(r'<a.*>Odhlásiť sa</a>', response.text)

def test_not_filled_user_data(test_client):
    data = {
        'username': '',
        'password': ''
    }

    response = test_client.post(url_for('site.login'), data=data)

    assert response.status_code == 400
    assert 'Vyplnte prihlásovacia údaje.' in response.text
    assert re.search(r'<a.*>Prihlásiť sa</a>', response.text)

def test_not_filled_username(test_client):
    data = {
        'username': '',
        'password': 'password'
    }

    response = test_client.post(url_for('site.login'), data=data)

    assert response.status_code == 400
    assert 'Vyplnte prihlásovacia údaje.' in response.text
    assert re.search(r'<a.*>Prihlásiť sa</a>', response.text)

def test_not_filled_password(test_client):
    data = {
        'username': 'username',
        'password': ''
    }

    response = test_client.post(url_for('site.login'), data=data)

    assert response.status_code == 400
    assert 'Vyplnte prihlásovacia údaje.' in response.text
    assert re.search(r'<a.*>Prihlásiť sa</a>', response.text)

def test_wrong_login_password(test_client):
    data = {
        'username': 'username',
        'password': 'test'
    }

    response = test_client.post(url_for('site.login'), data=data)

    assert response.status_code == 400
    assert 'Nesprávne prihlasovacie údaje.' in response.text
    assert re.search(r'<a.*>Prihlásiť sa</a>', response.text)

def test_wrong_login_username(test_client):
    data = {
        'username': 'test',
        'password': 'password'
    }

    response = test_client.post(url_for('site.login'), data=data)

    assert response.status_code == 400
    assert 'Nesprávne prihlasovacie údaje.' in response.text
    assert re.search(r'<a.*>Prihlásiť sa</a>', response.text)

def test_wrong_login_credentials(test_client):
    data = {
        'username': 'test',
        'password': 'test'
    }

    response = test_client.post(url_for('site.login'), data=data)

    assert response.status_code == 400
    assert 'Nesprávne prihlasovacie údaje.' in response.text
    assert re.search(r'<a.*>Prihlásiť sa</a>', response.text)
