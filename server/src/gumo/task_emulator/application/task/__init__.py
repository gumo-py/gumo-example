from logging import getLogger

from typing import List
from injector import inject

from gumo.task.domain import GumoTask
from gumo.task_emulator.application import TaskRepository

logger = getLogger(__name__)


class TaskFetchService:
    @inject
    def __init__(
            self,
            repository: TaskRepository,
    ):
        self._repository = repository

    def fetch(self) -> List[GumoTask]:
        return self._repository.fetch_list()
