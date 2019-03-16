from bookshelf.application.repository import BookRepository
from bookshelf.infrastructure.repository import DatastoreBookRepository


def bind(binder):
    binder.bind(BookRepository, to=DatastoreBookRepository)
