import mytest

from google.cloud import datastore

from gumo.core.injector import injector
from gumo.datastore.domain.entity_key import EntityKeyFactory
from gumo.datastore.domain.entity_key import EntityKey

from gumo.datastore.infrastructure.entity_key_mapper import EntityKeyMapper


key_mapper = injector.get(EntityKeyMapper)  # type: EntityKeyMapper


def test_to_datastore_key():
    entity_key = EntityKeyFactory().build_from_pairs(pairs=[
        ('Book', 'name'),
        ('BookComment', 'comment'),
    ])
    datastore_key = key_mapper.to_datastore_key(entity_key=entity_key)

    assert isinstance(datastore_key, datastore.Key), 'must be a datastore.Key'
    assert datastore_key.flat_path  == ('Book', 'name', 'BookComment', 'comment')
    assert datastore_key.kind == 'BookComment'
    assert datastore_key.name == 'comment'


def test_to_entity_key():
    datastore_key = datastore.Key(
        'Book', 'name', 'BookComment', 'comment',
        project='test-project'
    )
    entity_key = key_mapper.to_entity_key(datastore_key=datastore_key)

    assert isinstance(entity_key, EntityKey)
    assert entity_key.flat_pairs() == ['Book', 'name', 'BookComment', 'comment']
    assert entity_key.kind() == 'BookComment'
    assert entity_key.name() == 'comment'
