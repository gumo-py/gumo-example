import pytest

from gumo.datastore.domain.entity_key import RootKey
from gumo.datastore.domain.entity_key import EntityKey
from gumo.datastore.domain.entity_key import EntityKeyFactory

sample_key_pairs = [
    ('Book', 'name'),
    ('BookComment', 'comment'),
]


def test_zero_length_pairs():
    with pytest.raises(ValueError):
        EntityKeyFactory().build_from_pairs(pairs=[])


def test_pairs_to_key():
    key = EntityKeyFactory().build_from_pairs(pairs=sample_key_pairs)
    assert isinstance(key, EntityKey)
    assert len(key.pairs()) == 2
    assert key.kind() == 'BookComment'
    assert key.name() == 'comment'

    parent = key.parent()
    assert isinstance(parent, EntityKey)
    assert len(parent.pairs()) == 1
    assert parent.kind() == 'Book'
    assert parent.name() == 'name'

    root = parent.parent()
    assert isinstance(root, RootKey)
    assert len(root.pairs()) == 0
    assert root.kind() == 'Root'
    assert root.name() == 'root'
    assert root.parent() == root


def test_dict_pairs_to_key():
    key = EntityKeyFactory().build_from_pairs(pairs=[
        {'kind': 'Book', 'name': 'name'},
        {'kind': 'BookComment', 'name': 'comment'},
    ])
    assert isinstance(key, EntityKey)
    assert key.flat_pairs() == ['Book', 'name', 'BookComment', 'comment']

def test_flat_pairs():
    key = EntityKeyFactory().build_from_pairs(pairs=sample_key_pairs)
    assert key.flat_pairs() == ['Book', 'name', 'BookComment', 'comment']


def test_build():
    key = EntityKeyFactory().build(kind='Book', name='name')
    assert key.kind() == 'Book'
    assert key.name() == 'name'
    assert isinstance(key.parent(), RootKey)


def test_build_for_new():
    key = EntityKeyFactory().build_for_new(kind='Book')
    assert key.kind() == 'Book'
    assert isinstance(key.name(), str)
    assert len(key.name()) == 26
    assert isinstance(key.parent(), RootKey)


def test_entity_key_literal():
    key = EntityKeyFactory().build(kind='Book', name='name')
    assert key.key_literal() == "Key('Book', 'name')"
