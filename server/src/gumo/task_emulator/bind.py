from gumo.task_emulator.application.repository import TaskRepository
from gumo.task_emulator.infrastructure.repository import DatastoreTaskRepository


def bind(binder):
    binder.bind(TaskRepository, to=DatastoreTaskRepository)
