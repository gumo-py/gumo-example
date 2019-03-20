from gumo.core.domain import GumoConfiguration
from gumo.core import get_gumo_config


def bind(binder):
    binder.bind(GumoConfiguration, to=get_gumo_config())
