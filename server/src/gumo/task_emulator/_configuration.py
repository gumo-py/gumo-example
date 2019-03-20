import threading
from logging import getLogger

from gumo.core.injector import injector
from gumo.core import ConfigurationError
from gumo.task_emulator.domain.configuration import TaskEmulatorConfiguration


logger = getLogger('gumo.task')

_CONFIG = None
_CONFIG_LOCK = threading.RLock()


class ConfigurationFactory:
    @classmethod
    def build(
            cls,
            server_host: str,
    ) -> TaskEmulatorConfiguration:
        return TaskEmulatorConfiguration(
            server_host=server_host,
        )


def configure(**kwargs) -> TaskEmulatorConfiguration:
    global _CONFIG

    with _CONFIG_LOCK:
        if _CONFIG:
            raise ConfigurationError('Gumo.TaskEmulator is already configured.')

        _CONFIG = ConfigurationFactory.build(**kwargs)
        logger.debug(f'Gumo.TaskEmulator is configured, config={_CONFIG}')

        injector.binder.bind(TaskEmulatorConfiguration, to=_CONFIG)

        return _CONFIG


def configure_once(
        server_host: str,
) -> TaskEmulatorConfiguration:
    with _CONFIG_LOCK:
        if _CONFIG:
            return _CONFIG

        return configure(
            server_host=server_host,
        )


def is_configured() -> bool:
    with _CONFIG_LOCK:
        return _CONFIG is not None


def get_task_emulator_config() -> TaskEmulatorConfiguration:
    with _CONFIG_LOCK:
        if _CONFIG:
            return _CONFIG
        else:
            raise ConfigurationError('Gumo.TaskEmulator is not configured.')


def clear():
    global _CONFIG

    with _CONFIG_LOCK:
        if _CONFIG is None:
            return

        _CONFIG = None
        logger.debug('Cleared a Gumo.TaskEmulator configuration.')
