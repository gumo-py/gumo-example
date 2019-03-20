from typing import List

from bookshelf.application.book.repository import BookRepository

from bookshelf.domain import Book
from bookshelf.domain import fundamental

from gumo.datastore.infrastructure import DatastoreRepositoryMixin

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


class DatastoreBookRepository(BookRepository, DatastoreRepositoryMixin):
    def __init__(self):
        self._book_mapper = DatastoreBookMapper()

    def fetch_list(self) -> List[Book]:
        query = self.datastore_client.query(kind=Book.KIND)
        books = []

        for datastore_entity in query.fetch():
            books.append(self._book_mapper.to_entity(
                key=self.entity_key_mapper.to_entity_key(datastore_key=datastore_entity.key),
                doc=datastore_entity,
            ))

        return books

    def save(self, book: Book):
        datastore_key = self.entity_key_mapper.to_datastore_key(entity_key=book.key)
        e = self.DatastoreEntity(key=datastore_key)
        e.update(self._book_mapper.to_datastore_entity(book=book))
        self.datastore_client.put(e)
