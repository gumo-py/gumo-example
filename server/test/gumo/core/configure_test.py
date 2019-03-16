import pytest

from gumo.core import configure
from gumo.core import clear
from gumo.core._configuration import ConfigurationFactory
from gumo.core.domain import Configuration
from gumo.core.domain import GoogleCloudLocation
from gumo.core.domain import GoogleCloudProjectID
from gumo.core.exceptions import ConfigurationError


def test_configuration_factory_build():
    o = ConfigurationFactory.build(
        google_cloud_project='test-project',
        google_cloud_location='asia-northeast1'
    )

    assert o == Configuration(
        google_cloud_project=GoogleCloudProjectID('test-project'),
        google_cloud_location=GoogleCloudLocation('asia-northeast1'),
    )


def test_configuration_factory_build_failed():
    with pytest.raises(ValueError):
        ConfigurationFactory.build(
            google_cloud_project='test-project',
            google_cloud_location='unknown-location'
        )


def test_configure_duplicated():
    config = {
        'google_cloud_project': 'test-project',
        'google_cloud_location': 'asia-northeast1'
    }
    with pytest.raises(ConfigurationError):
        clear()
        configure(**config)
        configure(**config)
