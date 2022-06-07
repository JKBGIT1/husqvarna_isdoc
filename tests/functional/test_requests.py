def test_hello_world_request(test_client):
    response = test_client.get('/')
    assert b"<h2>Hello World!</h2>" in response.data