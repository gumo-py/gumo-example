import dataclasses


@dataclasses.dataclass(frozen=True)
class BookTitle:
    value: str

    MAX_TITLE_LENGTH = 1000

    def __post_init__(self):
        if self.value is None:
            raise ValueError('title must be present.')

        if len(self.value) > self.MAX_TITLE_LENGTH:
            raise ValueError(f'title is too long (length: {len(self.value)}, max length is {self.MAX_TITLE_LENGTH})')


@dataclasses.dataclass(frozen=True)
class BookAuthor:
    value: str

    MAX_AUTHOR_LENGTH = 200

    def __post_init__(self):
        if self.value is None:
            raise ValueError('author must be present.')

        if len(self.value) > self.MAX_AUTHOR_LENGTH:
            raise ValueError(f'author is too long (length: {len(self.value)}, max length is {self.MAX_AUTHOR_LENGTH})')


@dataclasses.dataclass(frozen=True)
class ISBN:
    value: str

    def __post_init__(self):
        # TODO: ISBN format check.
        pass
