from injector import inject
from typing import List

from gumo.core.domain import GumoConfiguration
from gumo.datastore.domain.configuration import DatastoreConfiguration
from gumo.task.domain.configuration import TaskConfiguration
from gumo.task_emulator.domain.configuration import TaskEmulatorConfiguration
from gumo.task.domain import GumoTask

from gumo.datastore import EntityKey
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

    def fetch_list(self) -> List[GumoTask]:
        raise NotImplementedError()

    def fetch_by_key(self, key: EntityKey) -> GumoTask:
        raise NotImplementedError()

    def fetch_by_name(self, name: str) -> GumoTask:
        key = self._entity_key_factory.build(kind=GumoTask.KIND, name=name)
        return self.fetch_by_key(key=key)

    def save(self, task: GumoTask) -> GumoTask:
        raise NotImplementedError()
