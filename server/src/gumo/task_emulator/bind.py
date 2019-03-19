from gumo.task_emulator.domain.configuration import TaskEmulatorConfiguration
from gumo.task_emulator._configuration import get_task_emulator_config

from gumo.task_emulator.application.repository import TaskRepository
from gumo.task_emulator.infrastructure.repository import DatastoreTaskRepository


def bind(binder):
    binder.bind(TaskEmulatorConfiguration, to=get_task_emulator_config)
    binder.bind(TaskRepository, to=DatastoreTaskRepository)
