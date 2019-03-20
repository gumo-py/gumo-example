from logging import getLogger

from gumo.core.injector import injector
from gumo.task_emulator.domain.configuration import TaskEmulatorConfiguration
from gumo.task_emulator.bind import task_emulator_bind


logger = getLogger('gumo.task')


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
    config = ConfigurationFactory.build(
        server_host=server_host
    )
    logger.debug(f'Gumo.TaskEmulator is configured, config={config}')

    injector.binder.bind(TaskEmulatorConfiguration, to=config)
    injector.binder.install(task_emulator_bind)

    return config
