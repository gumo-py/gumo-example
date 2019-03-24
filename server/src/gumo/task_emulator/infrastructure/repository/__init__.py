import datetime
from logging import getLogger

from injector import inject
from typing import List
from typing import Optional

from gumo.core.exceptions import ObjectNotoFoundError
from gumo.datastore import EntityKey
from gumo.datastore.infrastructure import DatastoreRepositoryMixin
from gumo.task.domain import GumoTask
from gumo.task.infrastructure.mapper import DatastoreGumoTaskMapper

from gumo.task_emulator.domain import GumoTaskProcess
from gumo.task_emulator.domain import TaskState
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

    def _fetch_list(self, query, limit: Optional[int] = None) -> List[GumoTask]:
        tasks = []

        for datastore_entity in query.fetch(limit=limit):
            tasks.append(self._task_mapper.to_entity(
                key=self.entity_key_mapper.to_entity_key(datastore_key=datastore_entity.key),
                doc=datastore_entity,
            ))

        return tasks

    def fetch_tasks(self, limit: int = 10) -> List[GumoTask]:
        return self._fetch_list(query=self._build_query(), limit=limit)

    def delete(self, key: EntityKey):
        datastore_key = self.entity_key_mapper.to_datastore_key(entity_key=key)
        self.datastore_client.delete(datastore_key)


class DatastoreTaskProcessRepository(TaskProcessRepository, DatastoreRepositoryMixin):
    @inject
    def __init__(
            self,
            task_process_mapper: DatastoreGumoTaskProcessMapper,
    ):
        super(DatastoreTaskProcessRepository, self).__init__()
        self._task_process_mapper = task_process_mapper

    def _build_query(self):
        return self.datastore_client.query(kind=GumoTaskProcess.KIND)

    def _fetch_query(self, query, limit) -> List[GumoTaskProcess]:
        task_processes = []
        for datastore_entity in query.fetch(limit=(limit or 10)):
            task_processes.append(
                self._task_process_mapper.to_entity(datastore_entity=datastore_entity)
            )

        return task_processes

    def fetch_by_key(self, key: EntityKey) -> GumoTaskProcess:
        datastore_key = self.entity_key_mapper.to_datastore_key(entity_key=key)
        datastore_entity = self.datastore_client.get(key=datastore_key)
        if datastore_entity is None:
            raise ObjectNotoFoundError(f'key={key} is not found.')

        entity = self._task_process_mapper.to_entity(datastore_entity=datastore_entity)
        return entity

    def fetch_tasks_by_state(self, state: TaskState, limit: Optional[int] = None) -> List[GumoTaskProcess]:
        now = datetime.datetime.utcnow().replace(microsecond=0)
        query = self._build_query()
        query.add_filter('state', '=', state.value)
        query.add_filter('run_at', '<=', now)
        query.order = ['run_at']

        task_processes = self._fetch_query(query=query, limit=limit)
        return task_processes

    def fetch_tasks(self, limit: Optional[int] = None) -> List[GumoTaskProcess]:
        query = self._build_query()

        task_processes = self._fetch_query(query=query, limit=limit)
        return task_processes

    def save(self, task_process: GumoTaskProcess):
        datastore_entity = self._task_process_mapper.to_datastore_entity(task_process=task_process)
        logger.debug(f'Datastore Put key={datastore_entity.key}')
        self.datastore_client.put(datastore_entity)
