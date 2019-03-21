from logging import getLogger

from injector import inject
from typing import List

from gumo.datastore.infrastructure import DatastoreRepositoryMixin
from gumo.task.domain import GumoTask
from gumo.task.infrastructure.mapper import DatastoreGumoTaskMapper

from gumo.task_emulator.domain import GumoTaskProcess
from gumo.task_emulator.application.task.repository import TaskRepository
from gumo.task_emulator.application.task.repository import TaskProcessRepository
from gumo.task_emulator.infrastructure.mapper import DatastoreGumoTaskProcessMapper

logger = getLogger(__name__)


class DatastoreTaskRepository(TaskRepository, DatastoreRepositoryMixin):
    @inject
    def __init__(
            self,
            gumo_task_mapper: DatastoreGumoTaskMapper,
    ):
        super(DatastoreTaskRepository, self).__init__()
        self._task_mapper = gumo_task_mapper

    def _build_query(self):
        return self.datastore_client.query(kind=GumoTask.KIND)

    def _fetch_list(self, query) -> List[GumoTask]:
        tasks = []

        for datastore_entity in query.fetch():
            tasks.append(self._task_mapper.to_entity(
                key=self.entity_key_mapper.to_entity_key(datastore_key=datastore_entity.key),
                doc=datastore_entity,
            ))

        return tasks

    def fetch_tasks(self) -> List[GumoTask]:
        return self._fetch_list(query=self._build_query())


class DatastoreTaskProcessRepository(TaskProcessRepository, DatastoreRepositoryMixin):
    @inject
    def __init__(
            self,
            task_process_mapper: DatastoreGumoTaskProcessMapper,
    ):
        super(DatastoreTaskProcessRepository, self).__init__()
        self._task_process_mapper = task_process_mapper

    def save(self, task_process: GumoTaskProcess):
        datastore_key = self.entity_key_mapper.to_datastore_key(entity_key=task_process.key)
        datastore_entity = self.DatastoreEntity(key=datastore_key)
        datastore_entity.update(
            self._task_process_mapper.to_datastore_entity(task_process=task_process)
        )
        self.datastore_client.put(datastore_entity)
