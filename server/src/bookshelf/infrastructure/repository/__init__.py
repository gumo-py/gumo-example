from typing import List

from bookshelf.application.book.repository import BookRepository

from bookshelf.domain import Book
from bookshelf.domain import fundamental

from gumo.datastore.infrastructure import DatastoreClient
from gumo.datastore.infrastructure import EntityKeyMapper

from gumo.datastore import EntityKey


class DatastoreBookMapper:
    def to_datastore_entity(self, book: Book) -> dict:
        j = {
            'title': book.title.value,
            'primary_author': book.primary_author.value,
            'authors': [
                author.value for author in book.authors
            ],
            'isbn': book.isbn.value,
        }

        return j

    def to_entity(self, key: EntityKey, doc: dict) -> Book:

        return Book(
            key=key,
            title=fundamental.BookTitle(doc.get('title')),
            primary_author=fundamental.BookAuthor(doc.get('primary_author')),
            authors=[
                fundamental.BookAuthor(a) for a in doc.get('authors', [])
            ],
            isbn=fundamental.ISBN(doc.get('isbn')),
        )


class DatastoreBookRepository(BookRepository):
    def __init__(self):
        self._client = DatastoreClient.get_instance()
        self._key_mapper = EntityKeyMapper()
        self._mapper = DatastoreBookMapper()

    def fetch_list(self) -> List[Book]:
        query = self._client.client.query(kind=Book.KIND)
        books = []

        for datastore_entity in query.fetch():
            books.append(self._mapper.to_entity(
                key=self._key_mapper.to_entity_key(datastore_key=datastore_entity.key),
                doc=datastore_entity,
            ))

        return books

    def save(self, book: Book):
        datastore_key = self._key_mapper.to_datastore_key(entity_key=book.key)
        e = self._client.Entity(key=datastore_key)
        e.update(self._mapper.to_datastore_entity(book=book))
        self._client.client.put(e)
