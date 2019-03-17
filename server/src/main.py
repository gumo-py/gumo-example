import os
import sys
import logging

import flask.views

from gumo.core import MockAppEngineEnvironment
from configuration import app_configure

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Initialization process in development environment.
if __name__ == '__main__' or 'PYTEST' in os.environ:
    app_yaml_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'app.yaml'
    )
    MockAppEngineEnvironment.load_app_yaml(app_yaml_path=app_yaml_path)

# Application framework initialization process.
app_configure()

app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def register_blueprints(application):
    from bookshelf.presentation import bookshelf_blueprint
    application.register_blueprint(bookshelf_blueprint)


register_blueprints(application=app)


@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    server_port = os.environ.get('SERVER_PORT', '8080')
    app.run(host='0.0.0.0', port=server_port, debug=True)
