from logging import getLogger
import flask.views

from gumo.core.injector import injector

from gumo.task_emulator.application.task import TaskFetchService
from gumo.task_emulator.application.task import TaskProcessBulkCreateService
from gumo.task_emulator.application.task.encoder import TaskJSONEncoder

logger = getLogger(__name__)
emulator_api_blueprint = flask.Blueprint('task-emulator', __name__)


class TasksView(flask.views.MethodView):
    _task_fetch_service = injector.get(TaskFetchService)  # type: TaskFetchService

    def get(self):
        tasks = self._task_fetch_service.fetch()

        return flask.jsonify({
            'results': [TaskJSONEncoder(task).to_json() for task in tasks]
        })

    def post(self):
        return 'ok'


class TasksEmulatorEnqueue(flask.views.MethodView):
    _task_process_create_service = injector.get(TaskProcessBulkCreateService)  # type: TaskProcessBulkCreateService

    def get(self):
        result = self._task_process_create_service.execute()
        return flask.jsonify(result)

    def post(self):
        result = self._task_process_create_service.execute()
        return flask.jsonify(result)


@emulator_api_blueprint.route('/')
def hello():
    return 'ok'


emulator_api_blueprint.add_url_rule(
    '/api/tasks',
    view_func=TasksView.as_view(name='tasks'),
    methods=['GET', 'POST']
)

emulator_api_blueprint.add_url_rule(
    '/api/tasks/emulator/enqueue',
    view_func=TasksEmulatorEnqueue.as_view(name='tasks/emulator/enqueue'),
    methods=['GET', 'POST']
)
