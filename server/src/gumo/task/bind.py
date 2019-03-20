from gumo.task.application.repository import GumoTaskRepository
from gumo.task.infrastructure.repository import GumoTaskRepositoryImpl

from gumo.task.domain.configuration import TaskConfiguration
from gumo.task import get_task_config


def bind(binder):
    binder.bind(GumoTaskRepository, to=GumoTaskRepositoryImpl)
    binder.bind(TaskConfiguration, to=get_task_config())
