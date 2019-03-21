from injector import inject
from typing import List

from gumo.core.domain import GumoConfiguration
from gumo.datastore.domain.configuration import DatastoreConfiguration
from gumo.task.domain.configuration import TaskConfiguration
from gumo.task_emulator.domain.configuration import TaskEmulatorConfiguration
from gumo.task.domain import GumoTask

from gumo.datastore import EntityKeyFactory


class TaskRepository:
    @inject
    def __init__(
            self,
            gumo_configuration: GumoConfiguration,
            datastore_configuration: DatastoreConfiguration,
            task_configuration: TaskConfiguration,
            task_emulator_configuration: TaskEmulatorConfiguration,
            entity_key_factory: EntityKeyFactory,
    ):
        self._gumo_configuration = gumo_configuration
        self._datastore_configuration = datastore_configuration
        self._task_configuration = task_configuration
        self._task_emulator_configuration = task_emulator_configuration
        self._entity_key_factory = entity_key_factory

    def fetch_tasks(self) -> List[GumoTask]:
        raise NotImplementedError()

    def save(self, task: GumoTask) -> GumoTask:
        raise NotImplementedError()
