from gumo.datastore.domain.entity_key import EntityKey
from google.cloud import datastore


class EntityKeyMapper:
    @classmethod
    def to_entity_key(cls, datastore_key: datastore.Key) -> EntityKey:
        raise NotImplementedError()

    @classmethod
    def to_datastore_key(cls, entity_key: EntityKey) -> datastore.Key:
        raise NotImplementedError()
