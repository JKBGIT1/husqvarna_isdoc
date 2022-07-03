import io

def test_file_not_uloaded(test_client):
    # firstly login user
    test_client.post('/', data={"username": "username", "password": "password"}, follow_redirects=True)

    response = test_client.post('/home')

    assert response.status_code == 400
    assert 'PDF súbor nebol nahratý. Použite Browse tlačidlo.' in response.text


def test_empty_form_uploaded(test_client):
    # firstly login user
    test_client.post('/', data={"username": "username", "password": "password"}, follow_redirects=True)

    data = {
        "pdf_file": (io.BytesIO(b''), '')
    }

    response = test_client.post('/home', content_type='multipart/form-data', data=data)

    assert response.status_code == 400
    assert 'PDF súbor nebol nahratý. Použite Browse tlačidlo.' in response.text


def test_not_husqvarna_pdf(test_client):
    # firstly login user
    test_client.post('/', data={"username": "username", "password": "password"}, follow_redirects=True)

    data = {
        "pdf_file": (io.BytesIO(b'test data'), 'test.pdf')
    }

    response = test_client.post('/home', data=data, content_type='multipart/form-data')

    assert response.status_code == 400
    assert 'Aplikácia narazila na problém, kontaktujte správcu.' in response.text