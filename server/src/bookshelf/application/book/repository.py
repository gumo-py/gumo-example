from typing import List

from bookshelf.domain import Book


class BookRepository:
    def fetch_list(self) -> List[Book]:
        raise NotImplementedError()

    def save(self, book: Book):
        raise NotImplementedError()
