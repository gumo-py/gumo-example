from logging import getLogger

from gumo.datastore._configuration import configure
from gumo.datastore._configuration import configure_once
from gumo.datastore._configuration import is_configured
from gumo.datastore._configuration import get_datastore_config
from gumo.datastore._configuration import clear
from gumo.datastore.domain.configuration import DatastoreConfiguration
from gumo.datastore.domain.entity_key import EntityKey


__all__ = [
    configure.__name__,
    configure_once.__name__,
    is_configured.__name__,
    get_datastore_config.__name__,
    clear.__name__,

    EntityKey.__name__,
    DatastoreConfiguration.__name__,
]

logger = getLogger('gumo.datastore')
