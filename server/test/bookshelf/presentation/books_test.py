import main
import json


def test_index():
    main.app.testing = True
    client = main.app.test_client()

    response = client.get('/books')
    assert response.status_code == 200
    books = json.loads(response.data.decode('utf-8'))
    assert len(books) == 1

    book = books[0]
    assert book['title'] == 'book title'
    assert book['primary_author'] == 'book primary author'
    assert book['isbn'] == '978-4-00-310101-8'
    assert len(book['authors']) == 1
