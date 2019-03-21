from gumo.task_emulator.application.task.repository import TaskRepository
from gumo.task_emulator.infrastructure.repository import DatastoreTaskRepository

from gumo.task_emulator.application.task.repository import TaskProcessRepository
from gumo.task_emulator.infrastructure.repository import DatastoreTaskProcessRepository


def task_emulator_bind(binder):
    binder.bind(TaskRepository, to=DatastoreTaskRepository)
    binder.bind(TaskProcessRepository, to=DatastoreTaskProcessRepository)
