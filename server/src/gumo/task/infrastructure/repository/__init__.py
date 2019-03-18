from typing import Optional

from gumo.task.application.repository import GumoTaskRepository

from gumo.task.domain import GumoTask


class DatastoreGumoTaskRepository(GumoTaskRepository):
    def _enqueue_to_cloud_tasks(
            self,
            task: GumoTask,
            queue_name: Optional[str] = None
    ):
        pass


    def _enqueue_to_local_emulator(
            self,
            task: GumoTask,
            queue_name: Optional[str] = None
    ):
        pass
