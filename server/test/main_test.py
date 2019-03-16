import main


def test_index():
    main.app.testing = True
    client = main.app.test_client()

    response = client.get('/')
    assert response.status_code == 200
    assert 'Hello, World!' in response.data.decode('utf-8')
