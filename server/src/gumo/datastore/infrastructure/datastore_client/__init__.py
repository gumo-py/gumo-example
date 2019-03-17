from gumo.core import get_gumo_config
from gumo.datastore import get_datastore_config

from google.cloud import datastore


class DatastoreClient:
    _instance = None
    Entity = datastore.Entity

    @classmethod
    def get_instance(cls):
        if cls._instance:
            return cls._instance
        cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._gumo_config = get_gumo_config()
        self._datastore_config = get_datastore_config()

        self._project = self._gumo_config.google_cloud_project.value
        self._namespace = self._datastore_config.namespace

        self.client = self._build_client()

    def _build_client(self) -> datastore.Client:
        return datastore.Client(
            project=self._project,
            namespace=self._namespace,
        )
