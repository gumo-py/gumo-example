import os
import threading
from logging import getLogger
from typing import Optional

from gumo.core.domain import GumoConfiguration
from gumo.core.domain import GoogleCloudLocation
from gumo.core.domain import GoogleCloudProjectID
from gumo.core.domain import ApplicationPlatform
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

        is_google_platform = 'GAE_DEPLOYMENT_ID' in os.environ and 'GAE_INSTANCE' in os.environ
        application_platform = ApplicationPlatform.GoogleAppEngine if is_google_platform else ApplicationPlatform.Local

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
            logger.debug(f'Environment Variable "GOOGLE_CLOUD_PROJECT" is update to {project_id}')

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
