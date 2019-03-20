from logging import getLogger

import flask.views

from injector import Injector

from bookshelf.application import BooksFetchService
from bookshelf.application import BookCreateService
from bookshelf.application.book.factory import BookFactory

from bookshelf.domain import Book

from bookshelf.bind import bind

logger = getLogger(__name__)
injector = Injector([bind])
bookshelf_blueprint = flask.Blueprint('bookshelf', __name__)


class BookJSONEncoder:
    def encode(self, book: Book):
        return {
            'key': book.key.key_literal(),
            'urlsafe_key': book.key.key_path_urlsafe(),
            'title': book.title.value,
            'primary_author': book.primary_author.value,
            'authors': [a.value for a in book.authors],
            'isbn': book.isbn.value,
        }


class BooksView(flask.views.MethodView):
    _fetch_service = injector.get(BooksFetchService)  # type: BooksFetchService
    _create_service = injector.get(BookCreateService)  # type: BookCreateService
    _factory = BookFactory()

    def get(self):
        books = self._fetch_service.fetch()

        return flask.jsonify([
            BookJSONEncoder().encode(book) for book in books
        ])

    def post(self):
        doc = flask.request.json
        request_book = self._factory.build_for_new(
            title=doc.get('title'),
            primary_author=doc.get('primary_author'),
            authors=doc.get('authors'),
            isbn=doc.get('isbn'),
        )

        book = self._create_service.create(request_book)
        return flask.jsonify(
            BookJSONEncoder().encode(book)
        )


bookshelf_blueprint.add_url_rule(
    '/books',
    view_func=BooksView.as_view(name='bookshelf/books'),
    methods=['GET', 'POST']
)
