import re

def test_login_logout_scenario(test_client):
    data = {
        "username": "username",
        "password": "password"
    }

    response = test_client.post('/', data=data, follow_redirects=True)

    assert len(response.history) == 1 # there has to be one redirect
    assert response.status_code == 200
    assert response.request.path == '/home'

    assert re.search(r'<a.*>Odhlásiť sa</a>', response.text)
    assert 'form action="" method="POST" enctype="multipart/form-data"' in response.text
    assert re.search(r'<button type="submit".*>Nahrať súbor</button>', response.text)

    response = test_client.get('/logout', data=data, follow_redirects=True)
    
    assert len(response.history) == 1
    assert response.status_code == 200
    assert response.request.path == '/'
    assert re.search(r'<a.*>Prihlásiť sa</a>', response.text)

