from logging import getLogger

import os
import flask.views
import flasgger
from celery import Celery

from gumo.task_emulator._configuration import configure
from gumo.task_emulator.domain.configuration import TaskEmulatorConfiguration


def task_emulator_app():
    from gumo.task_emulator.presentation.restapi import emulator_api_blueprint

    flask_app = flask.Flask(__name__)
    flask_app.config['JSON_AS_ASCII'] = False
    flask_app.config['SWAGGER'] = {
        'title': 'Task Emulator',
        'doc_dir': os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'apidoc',
        )
    }
    flask_app.config['CELERY_BROKER_URL'] = 'redis://redis:6379'
    flask_app.config['CELERY_BACKEND_URL'] = 'redis://redis:6379'

    flask_app.register_blueprint(emulator_api_blueprint)

    flasgger.Swagger(
        flask_app,
        template_file=os.path.join(flask_app.config['SWAGGER']['doc_dir'], 'template.yml')
    )

    celery = make_celery(flask_app)

    return flask_app, celery


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_BACKEND_URL'],
        broker=app.config['CELERY_BROKER_URL'],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


__all__ = [
    configure.__name__,

    TaskEmulatorConfiguration.__name__,

    task_emulator_app.__name__,
]

logger = getLogger('gumo.task_emulator')
