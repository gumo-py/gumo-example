from typing import List
from typing import Optional

from gumo.datastore import EntityKey
from gumo.task.domain import GumoTask
from gumo.task_emulator.domain import GumoTaskProcess
from gumo.task_emulator.domain import TaskState


class TaskRepository:
    def fetch_tasks(self, limit: int = 10) -> List[GumoTask]:
        raise NotImplementedError()

    def save(self, task: GumoTask) -> GumoTask:
        raise NotImplementedError()

    def delete(self, key: EntityKey):
        raise NotImplementedError()


class TaskProcessRepository:
    def fetch_by_key(self, key: EntityKey) -> GumoTaskProcess:
        raise NotImplementedError()

    def fetch_tasks_by_state(self, state: TaskState, limit: Optional[int] = None) -> List[GumoTaskProcess]:
        raise NotImplementedError()

    def fetch_tasks(self, limit: Optional[int] = None) -> List[GumoTaskProcess]:
        raise NotImplementedError()

    def save(self, task_process: GumoTaskProcess):
        raise NotImplementedError()
