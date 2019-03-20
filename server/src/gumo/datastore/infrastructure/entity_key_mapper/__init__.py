from injector import inject

from google.cloud import datastore

from gumo.core import GumoConfiguration

from gumo.datastore.domain.entity_key import EntityKey
from gumo.datastore.domain.entity_key import EntityKeyFactory


class EntityKeyMapper:
    @inject
    def __init__(
            self,
            gumo_config: GumoConfiguration,
            entity_key_factory: EntityKeyFactory,
    ):
        self._gumo_config = gumo_config
        self._entity_key_factory = entity_key_factory

    def to_entity_key(self, datastore_key: datastore.Key) -> EntityKey:
        entity_key = self._entity_key_factory.build_from_pairs(pairs=datastore_key.path)
        return entity_key

    def to_datastore_key(self, entity_key: EntityKey) -> datastore.Key:
        project = self._gumo_config.google_cloud_project.value
        datastore_key = datastore.Key(*entity_key.flat_pairs(), project=project)

        return datastore_key
