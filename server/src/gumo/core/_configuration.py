import os
import threading
from logging import getLogger
from typing import Optional

from gumo.core.domain import GumoConfiguration
from gumo.core.domain import GoogleCloudLocation
from gumo.core.domain import GoogleCloudProjectID
from gumo.core.exceptions import ConfigurationError

logger = getLogger('gumo.core')

_CONFIG = None
_CONFIG_LOCK = threading.RLock()  # Guards initialization.


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

        return GumoConfiguration(
            google_cloud_project=project_id,
            google_cloud_location=location,
        )


def configure(**kwargs):
    global _CONFIG

    with _CONFIG_LOCK:
        if _CONFIG:
            raise ConfigurationError('Gumo is already configured.')

        _CONFIG = ConfigurationFactory.build(**kwargs)
        logger.debug(f'Gumo is configured, config={_CONFIG}')
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


def get_gumo_config() -> GumoConfiguration:
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
