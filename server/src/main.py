import os
import sys
import logging

import flask.views

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    server_port = os.environ.get('SERVER_PORT', '8080')
    app.run(host='0.0.0.0', port=server_port, debug=True)
