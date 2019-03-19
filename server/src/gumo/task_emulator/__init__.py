from logging import getLogger

from gumo.task_emulator._configuration import configure
from gumo.task_emulator._configuration import configure_once
from gumo.task_emulator._configuration import is_configured
from gumo.task_emulator._configuration import get_task_emulator_config
from gumo.task_emulator._configuration import clear
from gumo.task_emulator.domain.configuration import TaskEmulatorConfiguration


__all__ = [
    configure.__name__,
    configure_once.__name__,
    is_configured.__name__,
    get_task_emulator_config.__name__,
    clear.__name__,

    TaskEmulatorConfiguration.__name__,
]

logger = getLogger('gumo.task_emulator')
