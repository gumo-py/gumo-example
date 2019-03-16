from logging import getLogger

import flask.views

from bookshelf.domain import Book
from bookshelf.domain import BookTitle
from bookshelf.domain import BookAuthor
from bookshelf.domain import ISBN

logger = getLogger(__name__)
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
    def get(self):
        book = Book(
            title=BookTitle('book title'),
            primary_author=BookAuthor('book primary author'),
            authors=[BookAuthor('book secondary author')],
            isbn=ISBN('978-4-00-310101-8'),
        )
        logger.info(f'book = {book}')

        return flask.jsonify([
            BookJSONEncoder().encode(book)
        ])

    def post(self):
        return flask.jsonify({})


bookshelf_blueprint.add_url_rule(
    '/books',
    view_func=BooksView.as_view(name='books'),
    methods=['GET', 'POST']
)
