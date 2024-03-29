import io
from flask import url_for

def login_user(test_client):
    test_client.post(url_for('site.login'), data={"username": "username", "password": "password"}, follow_redirects=True)

    return test_client

def test_file_not_uloaded(test_client):
    test_client = login_user(test_client)

    response = test_client.post(url_for('site.home'))

    print(response.text)

    assert response.status_code == 400
    assert 'PDF súbor nebol nahratý. Použite Browse tlačidlo.' in response.text


def test_empty_form_uploaded(test_client):
    test_client = login_user(test_client)

    data = {
        "pdf_file": (io.BytesIO(b''), '')
    }

    response = test_client.post(url_for('site.home'), content_type='multipart/form-data', data=data)

    assert response.status_code == 400
    assert 'PDF súbor nebol nahratý. Použite Browse tlačidlo.' in response.text


def test_not_husqvarna_pdf(test_client):
    test_client = login_user(test_client)

    data = {
        "pdf_file": (io.BytesIO(b'test data'), 'test.pdf')
    }

    response = test_client.post(url_for('site.home'), data=data, content_type='multipart/form-data')

    assert response.status_code == 400
    assert 'Aplikácia narazila na problém, kontaktujte správcu.' in response.text