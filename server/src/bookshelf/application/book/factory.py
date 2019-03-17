from typing import List
from typing import Optional

from bookshelf.domain import Book
from bookshelf.domain import fundamental
from gumo.datastore import EntityKey
from gumo.datastore import EntityKeyFactory


class BookFactory:
    def build(
            self,
            key: Optional[EntityKey] = None,
            title: Optional[str] = None,
            primary_author: Optional[str] = None,
            authors: List[str] = None,
            isbn: Optional[str] = None,
    ) -> Book:
        return Book(
            key=key,
            title=fundamental.BookTitle(title),
            primary_author=fundamental.BookAuthor(primary_author),
            authors=[
                fundamental.BookAuthor(a) for a in authors if a
            ] if authors else [],
            isbn=fundamental.ISBN(isbn),
        )

    def build_for_new(
            self,
            title: Optional[str] = None,
            primary_author: Optional[str] = None,
            authors: List[str] = None,
            isbn: Optional[str] = None,
    ) -> Book:
        key = EntityKeyFactory().build_for_new(kind=Book.KIND)

        return self.build(
            key=key,
            title=title,
            primary_author=primary_author,
            authors=authors,
            isbn=isbn,
        )
