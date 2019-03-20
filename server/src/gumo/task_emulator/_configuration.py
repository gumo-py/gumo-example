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


def configure(
        server_host: str,
) -> TaskEmulatorConfiguration:
    global _CONFIG

    with _CONFIG_LOCK:
        if _CONFIG:
            raise ConfigurationError('Gumo.TaskEmulator is already configured.')

        _CONFIG = ConfigurationFactory.build(
            server_host=server_host
        )
        logger.debug(f'Gumo.TaskEmulator is configured, config={_CONFIG}')

        injector.binder.bind(TaskEmulatorConfiguration, to=_CONFIG)

        return _CONFIG
