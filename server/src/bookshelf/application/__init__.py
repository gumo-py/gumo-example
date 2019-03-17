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

        # TODO: move to BookCreateService
        book = BookFactory().build_for_new(
            title=f'book title {datetime.datetime.now().isoformat()}',
            primary_author='sample author',
            isbn='978-1-234567-890',
        )

        self._repository.save(book)
        return books
