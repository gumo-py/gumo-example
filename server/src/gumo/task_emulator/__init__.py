from logging import getLogger

import os
import flask.views
import flasgger

from gumo.task_emulator._configuration import configure
from gumo.task_emulator._configuration import configure_once
from gumo.task_emulator._configuration import is_configured
from gumo.task_emulator._configuration import get_task_emulator_config
from gumo.task_emulator._configuration import clear
from gumo.task_emulator.domain.configuration import TaskEmulatorConfiguration

from gumo.task_emulator.presentation.restapi import emulator_api_blueprint


def task_emulator_app():
    flask_app = flask.Flask(__name__)
    flask_app.config['JSON_AS_ASCII'] = False
    flask_app.config['SWAGGER'] = {
        'title': 'Task Emulator',
        'doc_dir': os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'apidoc',
        )
    }
    flask_app.register_blueprint(emulator_api_blueprint)

    flasgger.Swagger(
        flask_app,
        template_file=os.path.join(flask_app.config['SWAGGER']['doc_dir'], 'template.yml')
    )

    return flask_app


__all__ = [
    configure.__name__,
    configure_once.__name__,
    is_configured.__name__,
    get_task_emulator_config.__name__,
    clear.__name__,

    TaskEmulatorConfiguration.__name__,

    task_emulator_app.__name__,
]

logger = getLogger('gumo.task_emulator')
