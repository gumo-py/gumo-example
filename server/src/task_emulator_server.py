import os
import sys
import logging

from gumo.core import MockAppEngineEnvironment
from configuration import app_configure
from gumo import task_emulator
from gumo.task_emulator import task_emulator_app

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialization process in development environment.
if __name__ == '__main__' or 'PYTEST' in os.environ:
    app_yaml_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'app.yaml'
    )
    MockAppEngineEnvironment.load_app_yaml(app_yaml_path=app_yaml_path)

# Application framework initialization process.
app_configure()
task_emulator.configure(
    server_host=os.environ.get('SERVER_HOST'),
    server_port=os.environ.get('SERVER_PORT'),
)

app = task_emulator_app()


if __name__ == '__main__':
    server_port = os.environ.get('TASK_EMULATOR_PORT', '8083')
    app.run(host='0.0.0.0', port=server_port, debug=True)
