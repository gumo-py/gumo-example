import datetime
from typing import Optional

from gumo.task.domain import GumoTask


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
