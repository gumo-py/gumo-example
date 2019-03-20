from logging import getLogger

from gumo.task._configuration import configure
from gumo.task._configuration import configure_once
from gumo.task._configuration import is_configured
from gumo.task._configuration import get_task_config
from gumo.task._configuration import clear
from gumo.task.domain.configuration import TaskConfiguration


__all__ = [
    configure.__name__,
    configure_once.__name__,
    is_configured.__name__,
    get_task_config.__name__,
    clear.__name__,

    TaskConfiguration.__name__,
]

logger = getLogger('gumo.task')
