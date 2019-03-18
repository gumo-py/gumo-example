import datetime
from typing import Optional

from injector import Injector

from gumo.task.domain import GumoTask

from gumo.task.application.factory import GumoTaskFactory
from gumo.task.application.repository import GumoTaskRepository

from gumo.task.bind import bind as task_bind

inject = Injector([task_bind])


def enqueue(
        url: str,
        method: str = 'POST',
        payload: Optional[dict] = None,
        schedule_time: Optional[datetime.datetime] = None,
        in_seconds: Optional[int] = None,
        queue_name: Optional[str] = None,
) -> GumoTask:
    task = GumoTaskFactory().build_for_new(
        url=url,
        method=method,
        payload=payload,
        schedule_time=schedule_time,
        in_seconds=in_seconds,
    )

    repository = inject.get(GumoTaskRepository)  # type: GumoTaskRepository
    repository.enqueue(task=task, queue_name=queue_name)

    return task
