import datetime
from typing import Optional

from gumo.task.domain import GumoTask
from gumo.task_emulator.domain import GumoTaskProcess
from gumo.task_emulator.domain import ProcessHistory


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


class TaskProcessJSONEncoder:
    def __init__(
            self,
            task_process: GumoTaskProcess,
    ):
        self._task_process = task_process

    def datetime_to_json(self, t: datetime.datetime) -> Optional[str]:
        if t is None:
            return
        return t.isoformat()

    def to_json(self) -> dict:
        j = {
            'key': self._task_process.key.key_path(),
            'keyLiteral': self._task_process.key.key_literal(),
            'relativeURI': self._task_process.relative_uri,
            'method': self._task_process.method,
            'payload': self._task_process.payload,
            'scheduleTime': self.datetime_to_json(self._task_process.schedule_time),
            'createdAt': self.datetime_to_json(self._task_process.created_at),
            'updatedAt': self.datetime_to_json(self._task_process.updated_at),
            'state': self._task_process.state.value,
            'attempts': self._task_process.attempts,
            'last_run_at': self.datetime_to_json(self._task_process.last_run_at),
            'run_at': self.datetime_to_json(self._task_process.run_at),
            'failed_at': self.datetime_to_json(self._task_process.failed_at),
            'histories': [
                self._history_to_json(history=history) for history in self._task_process.histories
            ],
        }
        return j

    def _history_to_json(self, history: ProcessHistory) -> dict:
        j = {
            'startedAt': self.datetime_to_json(history.started_at),
            'durationSeconds': history.duration_seconds,
            'statusCode': history.status_code,
            'requestHeader': history.request_header,
            'requestBody': history.request_body,
            'responseHeader': history.response_header,
            'responseBody': history.response_body,
        }
        return j
