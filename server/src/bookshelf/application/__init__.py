from logging import getLogger
from injector import inject

from typing import List

import datetime

from bookshelf.application.book.factory import BookFactory
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
        self._factory = BookFactory()

    def create(self, doc: dict) -> Book:
        book = self._factory.build_for_new(
            title=doc.get('title'),
            primary_author=doc.get('primary_author'),
            authors=doc.get('authors'),
            isbn=doc.get('isbn'),
        )

        self._repository.save(book=book)

        return book
