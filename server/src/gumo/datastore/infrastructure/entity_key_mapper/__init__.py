from google.cloud import datastore

from gumo.datastore.domain.entity_key import EntityKey
from gumo.datastore.domain.entity_key import EntityKeyFactory

from gumo.core import configure_once


class EntityKeyMapper:
    def to_entity_key(self, datastore_key: datastore.Key) -> EntityKey:
        entity_key = EntityKeyFactory().build_from_pairs(pairs=datastore_key.path)
        return entity_key

    def to_datastore_key(self, entity_key: EntityKey) -> datastore.Key:
        # TODO: configuration は DI で注入するようにしたい
        project = configure_once().google_cloud_project.value
        datastore_key = datastore.Key(*entity_key.flat_pairs(), project=project)

        return datastore_key
