import pytest

from gumo.datastore import configure
from gumo.datastore import clear
from gumo.datastore._configuration import ConfigurationFactory
from gumo.datastore.domain.configuration import DatastoreConfiguration
from gumo.core.exceptions import ConfigurationError


def test_configuration_factory_build():
    o = ConfigurationFactory.build(
        use_local_emulator='yes',
        emulator_host='localhost:8080',
        namespace='test',
    )

    assert o == DatastoreConfiguration(
        use_local_emulator=True,
        emulator_host='localhost:8080',
        namespace='test',
    )


def test_configuration_factory_build_failed():
    with pytest.raises(ValueError):
        ConfigurationFactory.build(
            use_local_emulator='yes',
            emulator_host=None,
            namespace='test',
        )


def test_configure_duplicated():
    config = {
        'use_local_emulator': 'yes',
        'emulator_host': 'localhost:8080',
        'namespace': 'test',
    }
    with pytest.raises(ConfigurationError):
        clear()
        configure(**config)
        configure(**config)
