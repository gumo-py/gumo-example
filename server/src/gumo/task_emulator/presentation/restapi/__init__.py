from logging import getLogger
import flask.views

from gumo.core.injector import injector

from gumo.task_emulator.application.task import TaskFetchService
from gumo.task_emulator.application.task import TaskProcessBulkCreateService
from gumo.task_emulator.application.task.encoder import TaskJSONEncoder
from gumo.task_emulator.application.task.encoder import TaskProcessJSONEncoder
from gumo.task_emulator.application.task.repository import TaskProcessRepository

from gumo.task_emulator.domain import TaskState

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


class QueuedTasksView(flask.views.MethodView):
    _repository = injector.get(TaskProcessRepository)  # type: TaskProcessRepository

    def get(self):
        task_processes = self._repository.fetch_tasks_by_state(state=TaskState.QUEUED)

        return flask.jsonify({
            'tasks': [TaskProcessJSONEncoder(task_process).to_json() for task_process in task_processes]
        })


@emulator_api_blueprint.route('/')
def hello():
    return 'ok'


emulator_api_blueprint.add_url_rule(
    '/api/tasks',
    view_func=TasksView.as_view(name='tasks'),
    methods=['GET', 'POST']
)

emulator_api_blueprint.add_url_rule(
    '/api/task_emulator/enqueue',
    view_func=TasksEmulatorEnqueue.as_view(name='task_emulator/enqueue'),
    methods=['GET', 'POST']
)

emulator_api_blueprint.add_url_rule(
    '/api/task_emulator/tasks/queued',
    view_func=QueuedTasksView.as_view(name='task_emulator/tasks/queued'),
    methods=['GET']
)
