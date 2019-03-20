import threading
from logging import getLogger

from typing import Optional
from typing import Union

from gumo.core.injector import injector
from gumo.core import ConfigurationError
from gumo.datastore.domain.configuration import DatastoreConfiguration


logger = getLogger('gumo.datastore')

_CONFIG = None
_CONFIG_LOCK = threading.RLock()


class ConfigurationFactory:
    @classmethod
    def build(
            cls,
            use_local_emulator: Union[str, bool, None] = None,
            emulator_host: Optional[str] = None,
            namespace: Optional[str] = None,
    ) -> DatastoreConfiguration:
        _use_emulator = False
        if isinstance(use_local_emulator, bool):
            _use_emulator = use_local_emulator
        elif isinstance(use_local_emulator, str):
            _use_emulator = use_local_emulator.lower() in ['true', 'yes']

        return DatastoreConfiguration(
            use_local_emulator=_use_emulator,
            emulator_host=emulator_host,
            namespace=namespace,
        )


def configure(**kwargs) -> DatastoreConfiguration:
    global _CONFIG

    with _CONFIG_LOCK:
        if _CONFIG:
            raise ConfigurationError('Gumo.Datastore is already configured.')

        _CONFIG = ConfigurationFactory.build(**kwargs)
        logger.debug(f'Gumo.Datastore is configured, config={_CONFIG}')

        injector.binder.bind(DatastoreConfiguration, to=_CONFIG)

        return _CONFIG


def configure_once(
        use_local_emulator: Union[str, bool, None] = None,
        emulator_host: Optional[str] = None,
        namespace: Optional[str] = None,
) -> DatastoreConfiguration:
    with _CONFIG_LOCK:
        if _CONFIG:
            return _CONFIG

        return configure(
            use_local_emulator=use_local_emulator,
            emulator_host=emulator_host,
            namespace=namespace,
        )


def is_configured() -> bool:
    with _CONFIG_LOCK:
        return _CONFIG is not None


def get_datastore_config() -> DatastoreConfiguration:
    with _CONFIG_LOCK:
        if _CONFIG:
            return _CONFIG
        else:
            raise ConfigurationError('Gumo.Datastore is not configured.')


def clear():
    global _CONFIG

    with _CONFIG_LOCK:
        if _CONFIG is None:
            return

        _CONFIG = None
        logger.debug('Cleared a Gumo.Datastore configuration.')
