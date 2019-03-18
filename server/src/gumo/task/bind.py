from gumo.task.application.repository import GumoTaskRepository
from gumo.task.infrastructure.repository import DatastoreGumoTaskRepository

from gumo.task.domain.configuration import TaskConfiguration
from gumo.task import get_task_config

def bind(binder):
    binder.bind(GumoTaskRepository, to=DatastoreGumoTaskRepository)
    binder.bind(TaskConfiguration, to=get_task_config())
