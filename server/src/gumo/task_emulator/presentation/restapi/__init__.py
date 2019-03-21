from logging import getLogger
import flask.views
import datetime
from typing import Optional

from gumo.core.injector import injector

from gumo.task.domain import GumoTask
from gumo.task_emulator.application.task import TaskFetchService
from gumo.task_emulator.application.task import TaskProcessBulkCreateService

logger = getLogger(__name__)
emulator_api_blueprint = flask.Blueprint('task-emulator', __name__)


class TaskJSONEncoder:
    def __init__(
            self,
            task: GumoTask,
    ):
        self._task = task

    def datetime_to_json(self, t: datetime.datetime) -> Optional[str]:
        if t is None:
            return
        return t.isoformat()

    def to_json(self) -> dict:
        j = {
            'key': self._task.key.key_path(),
            'keyLiteral': self._task.key.key_literal(),
            'relativeURI': self._task.relative_uri,
            'method': self._task.method,
            'payload': self._task.payload,
            'scheduleTime': self.datetime_to_json(self._task.schedule_time),
            'createdAt': self.datetime_to_json(self._task.created_at),
        }
        return j


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
        task_processes = self._task_process_create_service.execute()
        return ''

    def post(self):
        return ''


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
