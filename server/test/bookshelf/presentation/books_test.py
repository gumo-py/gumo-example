import mytest
import json


def test_index():
    response = mytest.client.get('/books')

    assert response.status_code == 200
    books = json.loads(response.data.decode('utf-8'))
    assert isinstance(books, list)
