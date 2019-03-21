from typing import List
from gumo.task.domain import GumoTask

from gumo.datastore import EntityKeyFactory


class TaskRepository:
    def fetch_tasks(self) -> List[GumoTask]:
        raise NotImplementedError()

    def save(self, task: GumoTask) -> GumoTask:
        raise NotImplementedError()
