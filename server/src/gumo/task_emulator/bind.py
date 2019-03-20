from gumo.task_emulator.application.repository import TaskRepository
from gumo.task_emulator.infrastructure.repository import DatastoreTaskRepository


def task_emulator_bind(binder):
    binder.bind(TaskRepository, to=DatastoreTaskRepository)
