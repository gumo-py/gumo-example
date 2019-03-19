from gumo.core import get_gumo_config
from gumo.core import GumoConfiguration
from gumo.datastore import get_datastore_config

from gumo.datastore.infrastructure.entity_key_mapper import EntityKeyMapper

from google.cloud import datastore


class DatastoreRepositoryMixin:
    _datastore_client = None
    _entity_key_mapper = None

    DatastoreEntity = datastore.Entity

    @property
    def datastore_client(self) -> datastore.Client:
        if self._datastore_client is None:
            gumo_config = get_gumo_config(GumoConfiguration)
            datastore_config = get_datastore_config()

            self._datastore_client = datastore.Client(
                project=gumo_config.google_cloud_project.value,
                namespace=datastore_config.namespace,
            )

        return self._datastore_client

    @property
    def entity_key_mapper(self) -> EntityKeyMapper:
        if self._entity_key_mapper is None:
            self._entity_key_mapper = EntityKeyMapper()

        return self._entity_key_mapper
