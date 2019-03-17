import dataclasses

from typing import List

from gumo.datastore import EntityKey

from bookshelf.domain.fundamental import BookTitle
from bookshelf.domain.fundamental import BookAuthor
from bookshelf.domain.fundamental import ISBN


@dataclasses.dataclass(frozen=True)
class Book:
    key: EntityKey
    title: BookTitle
    primary_author: BookAuthor
    authors: List[BookAuthor]
    isbn: ISBN

    KIND = 'Book'
