from typing import List

from bookshelf.application.repository import BookRepository

from bookshelf.domain import Book
from bookshelf.domain import BookTitle
from bookshelf.domain import BookAuthor
from bookshelf.domain import ISBN


class DatastoreBookRepository(BookRepository):
    def fetch_list(self) -> List[Book]:
        book = Book(
            title=BookTitle('book title'),
            primary_author=BookAuthor('book primary author'),
            authors=[BookAuthor('book secondary author')],
            isbn=ISBN('978-4-00-310101-8'),
        )

        return [book]
