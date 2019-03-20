import threading
from logging import getLogger

from typing import Union

from gumo.core.injector import injector
from gumo.core import ConfigurationError
from gumo.task.domain.configuration import TaskConfiguration


logger = getLogger('gumo.task')

_CONFIG = None
_CONFIG_LOCK = threading.RLock()


class ConfigurationFactory:
    @classmethod
    def build(
            cls,
            default_queue_name: str,
            use_local_task_emulator: Union[str, bool, None] = False
    ) -> TaskConfiguration:
        use_emulator = False

        if isinstance(use_local_task_emulator, bool):
            use_emulator = use_local_task_emulator
        elif isinstance(use_local_task_emulator, str):
            use_emulator = use_local_task_emulator.lower() in ['true', 'yes']

        return TaskConfiguration(
            default_queue_name=default_queue_name,
            use_local_task_emulator=use_emulator,
        )


def configure(**kwargs) -> TaskConfiguration:
    global _CONFIG

    with _CONFIG_LOCK:
        if _CONFIG:
            raise ConfigurationError('Gumo.Task is already configured.')

        _CONFIG = ConfigurationFactory.build(**kwargs)
        logger.debug(f'Gumo.Task is configured, config={_CONFIG}')

        injector.binder.bind(TaskConfiguration, to=_CONFIG)

        return _CONFIG


def configure_once(
        default_queue_name: str,
        use_local_task_emulator: Union[str, bool, None] = False
) -> TaskConfiguration:
    with _CONFIG_LOCK:
        if _CONFIG:
            return _CONFIG

        return configure(
            default_queue_name=default_queue_name,
            use_local_task_emulator=use_local_task_emulator,
        )


def is_configured() -> bool:
    with _CONFIG_LOCK:
        return _CONFIG is not None


def get_task_config() -> TaskConfiguration:
    with _CONFIG_LOCK:
        if _CONFIG:
            return _CONFIG
        else:
            raise ConfigurationError('Gumo.Task is not configured.')


def clear():
    global _CONFIG

    with _CONFIG_LOCK:
        if _CONFIG is None:
            return

        _CONFIG = None
        logger.debug('Cleared a Gumo.Task configuration.')
