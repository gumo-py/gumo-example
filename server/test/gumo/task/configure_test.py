import pytest

from gumo.task import configure
from gumo.task._configuration import ConfigurationFactory
from gumo.task.domain.configuration import TaskConfiguration
from gumo.core.exceptions import ConfigurationError


def test_configuration_factory_build():
    o = ConfigurationFactory.build(
        default_queue_name='gumo-default-queue',
        use_local_task_emulator='yes',
    )

    assert o == TaskConfiguration(
        default_queue_name='gumo-default-queue',
        use_local_task_emulator=True,
    )


def test_configure_duplicated():
    config = {
        'use_local_task_emulator': 'yes',
        'default_queue_name': 'gumo-default-queue'
    }
    with pytest.raises(ConfigurationError):
        configure(**config)
        configure(**config)
