from logging import getLogger

import flask.views

from injector import Injector

from bookshelf.application import BooksFetchService
from bookshelf.application import BookCreateService

from bookshelf.domain import Book

from bookshelf.bind import bind

logger = getLogger(__name__)
injector = Injector([bind])
bookshelf_blueprint = flask.Blueprint('bookshelf', __name__)


class BookJSONEncoder:
    def encode(self, book: Book):
        return {
            'title': book.title.value,
            'primary_author': book.primary_author.value,
            'authors': [a.value for a in book.authors],
            'isbn': book.isbn.value,
        }


class BooksView(flask.views.MethodView):
    _fetch_service = injector.get(BooksFetchService)  # type: BooksFetchService
    _create_service = injector.get(BookCreateService)  # type: BookCreateService

    def get(self):
        books = self._fetch_service.fetch()

        return flask.jsonify([
            BookJSONEncoder().encode(book) for book in books
        ])

    def post(self):
        j = flask.request.json
        book = self._create_service.create(doc=j)
        return flask.jsonify(
            BookJSONEncoder().encode(book)
        )


bookshelf_blueprint.add_url_rule(
    '/books',
    view_func=BooksView.as_view(name='books'),
    methods=['GET', 'POST']
)
