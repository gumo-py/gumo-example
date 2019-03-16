import mytest


def test_index():
    response = mytest.client.get('/')
    assert response.status_code == 200
    assert 'Hello, World!' in response.data.decode('utf-8')
