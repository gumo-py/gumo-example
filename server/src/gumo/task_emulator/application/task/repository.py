from typing import List
from gumo.task.domain import GumoTask
from gumo.task_emulator.domain import GumoTaskProcess


class TaskRepository:
    def fetch_tasks(self) -> List[GumoTask]:
        raise NotImplementedError()

    def save(self, task: GumoTask) -> GumoTask:
        raise NotImplementedError()


class TaskProcessRepository:
    def save(self, task_process: GumoTaskProcess):
        raise NotImplementedError()
