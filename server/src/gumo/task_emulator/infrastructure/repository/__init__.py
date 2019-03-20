from logging import getLogger

from injector import inject
from typing import List

from gumo.datastore.infrastructure import DatastoreRepositoryMixin
from gumo.task.domain import GumoTask
from gumo.task.infrastructure.mapper import DatastoreGumoTaskMapper

from gumo.task_emulator.application.task.repository import TaskRepository

logger = getLogger(__name__)


class DatastoreTaskRepository(TaskRepository, DatastoreRepositoryMixin):
    @inject
    def __init__(
            self,
            gumo_task_mapper: DatastoreGumoTaskMapper,
    ):
        super(DatastoreTaskRepository, self).__init__()
        self._task_mapper = gumo_task_mapper

    def fetch_list(self) -> List[GumoTask]:
        query = self.datastore_client.query(kind=GumoTask.KIND)
        tasks = []

        for datastore_entity in query.fetch():
            tasks.append(self._task_mapper.to_entity(
                key=self.entity_key_mapper.to_entity_key(datastore_key=datastore_entity.key),
                doc=datastore_entity,
            ))

        return tasks
