from gumo.datastore.infrastructure.client_factory import ClientFactory
from gumo.datastore.infrastructure.entity_key_mapper import EntityKeyMapper


client = ClientFactory().client()

__all__ = [
    EntityKeyMapper.__name__,
    client.__name__,
]
