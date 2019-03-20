import datetime
from typing import Optional

from logging import getLogger

from injector import Injector

from gumo.task.domain import GumoTask

from gumo.task.application.factory import GumoTaskFactory
from gumo.task.application.repository import GumoTaskRepository

from gumo.core.bind import bind as core_bind
from gumo.datastore.bind import bind as datastore_bind
from gumo.task.bind import bind as task_bind

logger = getLogger(__name__)
inject = Injector([
    core_bind,
    datastore_bind,
    task_bind,
])


def enqueue(
        url: str,
        method: str = 'POST',
        payload: Optional[dict] = None,
        schedule_time: Optional[datetime.datetime] = None,
        in_seconds: Optional[int] = None,
        queue_name: Optional[str] = None,
) -> GumoTask:
    task = GumoTaskFactory().build_for_new(
        relative_uri=url,
        method=method,
        payload=payload,
        schedule_time=schedule_time,
        in_seconds=in_seconds,
    )

    logger.info(f'gumo.task.enqueue called. task = {task}')

    repository = inject.get(GumoTaskRepository)  # type: GumoTaskRepository
    repository.enqueue(task=task, queue_name=queue_name)

    return task
