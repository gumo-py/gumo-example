import datetime
from typing import Optional

from logging import getLogger

from gumo.core.injector import injector
from gumo.task.domain import GumoTask

from gumo.task.application.factory import GumoTaskFactory
from gumo.task.application.repository import GumoTaskRepository

logger = getLogger(__name__)


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
        queue_name=queue_name,
    )

    logger.info(f'gumo.task.enqueue called. task = {task}')

    repository = injector.get(GumoTaskRepository)  # type: GumoTaskRepository
    repository.enqueue(task=task, queue_name=queue_name)

    return task
