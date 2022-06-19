def test_required_login(test_client):
    response = test_client.get('/home', follow_redirects=True)

    assert len(response.history) == 1
    assert response.status_code == 200
    assert 'Pre túto akciu je potrebné prihlásenie.' in response.text
