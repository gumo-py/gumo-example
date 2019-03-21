from logging import getLogger

from typing import List
from injector import inject

from gumo.task.domain import GumoTask

from gumo.task_emulator.domain import GumoTaskProcess
from gumo.task_emulator.domain import GumoTaskProcessFactory
from gumo.task_emulator.application.task.repository import TaskRepository
from gumo.task_emulator.application.task.repository import TaskProcessRepository

logger = getLogger(__name__)


class TaskFetchService:
    @inject
    def __init__(
            self,
            repository: TaskRepository,
    ):
        self._repository = repository

    def fetch(self) -> List[GumoTask]:
        return self._repository.fetch_tasks()


class TaskProcessBulkCreateService:
    @inject
    def __init__(
            self,
            task_repository: TaskRepository,
            task_process_repository: TaskProcessRepository,
            task_process_factory: GumoTaskProcessFactory,
    ):
        self._task_repository = task_repository
        self._task_process_repository = task_process_repository
        self._task_process_factory = task_process_factory

    def execute(self) -> List[GumoTaskProcess]:
        tasks = self._task_repository.fetch_tasks()
        task_processes = []

        logger.info(f'Convert from GumoTask to GumoTaskProcess {len(tasks)} items.')

        for task in tasks:
            task_processes.append(
                self._execute(task=task)
            )

        return task_processes

    def _execute(self, task: GumoTask) -> GumoTaskProcess:
        logger.debug(f'Task.key={task.key} convert to GumoTaskProcess ...')
        task_process = self._task_process_factory.build_from_task(task=task)
        self._task_process_repository.save(task_process=task_process)
        logger.debug(f'[GumoTaskProcess Created] GumoTaskProcess.key={task_process.key}')

        return task_process
