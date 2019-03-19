from logging import getLogger
import flask.views

from gumo.core import get_injector

from gumo.task_emulator.application import TaskFetchService

logger = getLogger(__name__)
injector = get_injector()
emulator_api_blueprint = flask.Blueprint('task-emulator', __name__)


class TasksView(flask.views.MethodView):
    def get(self):
        _task_fetch_service = injector.get(TaskFetchService)  # type: TaskFetchService
        logger.info(_task_fetch_service)
        return 'ok'

    def post(self):
        return 'ok'


emulator_api_blueprint.add_url_rule(
    '/',
    view_func=TasksView.as_view(name='tasks'),
    methods=['GET', 'POST']
)
