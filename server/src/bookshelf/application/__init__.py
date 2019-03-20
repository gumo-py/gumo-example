from logging import getLogger
from injector import inject

from typing import List

from bookshelf.application.book.repository import BookRepository

from bookshelf.domain import Book

logger = getLogger(__name__)


class BooksFetchService:
    @inject
    def __init__(
            self,
            repository: BookRepository,
    ):
        self._repository = repository

    def fetch(self) -> List[Book]:
        books = self._repository.fetch_list()
        return books


class BookCreateService:
    @inject
    def __init__(
            self,
            repository: BookRepository,
    ):
        self._repository = repository

    def create(self, book: Book) -> Book:
        self._repository.save(book=book)

        # something process ...

        return book
