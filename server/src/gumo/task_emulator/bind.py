from gumo.task_emulator.domain.configuration import TaskEmulatorConfiguration
from gumo.task_emulator._configuration import get_task_emulator_config


def bind(binder):
    binder.bind(TaskEmulatorConfiguration, to=get_task_emulator_config())
