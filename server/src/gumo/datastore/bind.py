from gumo.datastore import DatastoreConfiguration
from gumo.datastore import get_datastore_config


def bind(binder):
    binder.bind(DatastoreConfiguration, to=get_datastore_config)
