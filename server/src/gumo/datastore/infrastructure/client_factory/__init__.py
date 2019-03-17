from gumo.core import get_gumo_config
from gumo.datastore import get_datastore_config

from google.cloud import datastore


class ClientFactory:
    def __init__(self):
        self._gumo_config = get_gumo_config()
        self._datastore_config = get_datastore_config()

        self._project = self._gumo_config.google_cloud_project.value
        self._namespace = self._datastore_config.namespace

    def client(self):
        if self._datastore_config.use_local_emulator:
            return self._build_mock_client()
        else:
            return self._build_client()

    def _build_client(self) -> datastore.Client:
        return datastore.Client(
            project=self._project,
            namespace=self._namespace,
        )

    def _build_mock_client(self) -> datastore.Client:
        import mock
        import google.auth.credentials
        import os
        os.environ.set('DATASTORE_EMULATOR_HOST', self._datastore_config.emulator_host)
        credentials = mock.Mock(spec=google.auth.credentials.Credentials)
        return datastore.Client(
            credentials=credentials,
            namespace=self._namespace,
        )
