import dataclasses

from typing import List

from bookshelf.domain.fundamental import BookTitle
from bookshelf.domain.fundamental import BookAuthor
from bookshelf.domain.fundamental import ISBN


@dataclasses.dataclass(frozen=True)
class Book:
    title: BookTitle
    primary_author: BookAuthor
    authors: List[BookAuthor]
    isbn: ISBN
