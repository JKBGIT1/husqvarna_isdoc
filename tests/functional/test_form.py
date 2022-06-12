def test_login_form(test_client):
    response = test_client.get('/')
    assert response.status_code == 200

    page_content = response.data

    labels = ['Používateľské meno', 'Heslo']
    for label in labels:
        assert label in page_content