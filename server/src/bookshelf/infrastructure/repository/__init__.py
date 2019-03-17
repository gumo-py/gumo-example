from typing import List

from bookshelf.application.book.repository import BookRepository

from bookshelf.domain import Book
from bookshelf.domain import BookTitle
from bookshelf.domain import BookAuthor
from bookshelf.domain import ISBN

from gumo.datastore.infrastructure import DatastoreClient
from gumo.datastore.infrastructure import EntityKeyMapper

from gumo.datastore import EntityKeyFactory


class DatastoreBookRepository(BookRepository):
    def __init__(self):
        self._client = DatastoreClient.get_instance()

    def fetch_list(self) -> List[Book]:
        book = Book(
            key=EntityKeyFactory().build_from_pairs([('Book', 'value')]),
            title=BookTitle('book title'),
            primary_author=BookAuthor('book primary author'),
            authors=[BookAuthor('book secondary author')],
            isbn=ISBN('978-4-00-310101-8'),
        )

        return [book]

    def save(self, book: Book):
        datastore_key = EntityKeyMapper().to_datastore_key(entity_key=book.key)
        e = self._client.Entity(key=datastore_key)
        e.update({
            'title': 'book title'
        })
        self._client.client.put(e)
