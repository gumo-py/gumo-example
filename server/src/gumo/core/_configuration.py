import os
import threading
from logging import getLogger
from typing import Optional
from injector import Injector

from gumo.core.domain import GumoConfiguration
from gumo.core.domain import GoogleCloudLocation
from gumo.core.domain import GoogleCloudProjectID
from gumo.core.domain import ApplicationPlatform
from gumo.core.exceptions import ConfigurationError

logger = getLogger('gumo.core')

_CONFIG = None
_CONFIG_LOCK = threading.RLock()  # Guards initialization.

_BIND_CONFIG = []
_BIND_LOCK = threading.RLock()

_INJECTOR = None
_INJECTOR_LOCK = threading.RLock()

_GUMO_CONFIGS = {}
_GUMO_CONFIGS_LOCK = threading.RLock()


def activate_gumo_module(interface, config):
    with _GUMO_CONFIGS_LOCK:
        _GUMO_CONFIGS[interface] = config


def get_gumo_config(interface):
    with _GUMO_CONFIGS_LOCK:
        if interface in _GUMO_CONFIGS:
            return _GUMO_CONFIGS[interface]()

        raise ConfigurationError(f'Gumo {interface} is not configured.')


def append_binding(binder):
    global _BIND_CONFIG
    global _INJECTOR

    with _BIND_LOCK:
        logger.debug(f'append binding={binder}, {binder.__module__}')
        _BIND_CONFIG.append(binder)

        with _INJECTOR_LOCK:
            _INJECTOR = Injector(_BIND_CONFIG)

        return _BIND_CONFIG


def get_bindings():
    with _BIND_LOCK:
        return _BIND_CONFIG


def get_injector():
    with _INJECTOR_LOCK:
        return _INJECTOR


class ConfigurationFactory:
    @classmethod
    def build(
            cls,
            google_cloud_project: Optional[str] = None,
            google_cloud_location: Optional[str] = None,
    ) -> GumoConfiguration:

        project_id = GoogleCloudProjectID(
            google_cloud_project if google_cloud_project else os.environ.get('GOOGLE_CLOUD_PROJECT')
        )

        location = GoogleCloudLocation(
            google_cloud_location if google_cloud_location else os.environ.get('GOOGLE_CLOUD_LOCATION')
        )

        is_google_platform = 'GAE_DEPLOYMENT_ID' in os.environ and 'GAE_INSTANCE' in os.environ
        application_platform = ApplicationPlatform.GoogleAppEngine if is_google_platform else ApplicationPlatform.Local

        if application_platform == ApplicationPlatform.Local:
            if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
                raise ConfigurationError('Envrionment variable "GOOGLE_APPLICATION_CREDENTIALS" is required.')

        return GumoConfiguration(
            google_cloud_project=project_id,
            google_cloud_location=location,
            application_platform=application_platform,
        )


def configure(**kwargs):
    global _CONFIG

    with _CONFIG_LOCK:
        if _CONFIG:
            raise ConfigurationError('Gumo is already configured.')

        _CONFIG = ConfigurationFactory.build(**kwargs)
        logger.debug(f'Gumo is configured, config={_CONFIG}')

        if 'GOOGLE_CLOUD_PROJECT' not in os.environ:
            logger.debug('Environment Variable "GOOGLE_CLOUD_PROJECT" is not configured.')
            project_id = _CONFIG.google_cloud_project.value
            os.environ['GOOGLE_CLOUD_PROJECT'] = project_id
            logger.debug(f'Environment Variable "GOOGLE_CLOUD_PROJECT" has been updated to {project_id}')

        def binder(binder):
            binder.bind(GumoConfiguration, to=get_core_config)

        append_binding(binder)
        activate_gumo_module(GumoConfiguration, get_core_config)

        return _CONFIG


def configure_once(
        google_cloud_project: Optional[str] = None,
        google_cloud_location: Optional[str] = None,
):
    with _CONFIG_LOCK:
        if _CONFIG:
            return _CONFIG

        return configure(
            google_cloud_project=google_cloud_project,
            google_cloud_location=google_cloud_location,
        )


def is_configured():
    with _CONFIG_LOCK:
        return _CONFIG is not None


def get_core_config() -> GumoConfiguration:
    with _CONFIG_LOCK:
        if _CONFIG:
            return _CONFIG
        else:
            raise ConfigurationError('Gumo is not configured.')


def clear():
    global _CONFIG

    with _CONFIG_LOCK:
        if _CONFIG is None:
            return

        _CONFIG = None
        logger.debug('Cleared a gumo configuration.')
