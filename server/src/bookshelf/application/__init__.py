from logging import getLogger
from injector import inject

from typing import List

from bookshelf.application.repository import BookRepository

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
        # TODO: permission check
        return books
