from injector import inject

from gumo.datastore.infrastructure import DatastoreEntity
from gumo.datastore.infrastructure import EntityKeyMapper
from gumo.task_emulator.domain import GumoTaskProcess
from gumo.task_emulator.domain import ProcessHistory
from gumo.task_emulator.domain import TaskState


class DatastoreGumoProcessHistoryMapper:
    def to_datastore_entity(self, process_history: ProcessHistory) -> dict:
        j = {
            'started_at': process_history.started_at,
            'duration_seconds': process_history.duration_seconds,
            'status_code': process_history.status_code,
            'request_header': process_history.request_header,
            'request_body': process_history.request_body,
            'response_header': process_history.response_header,
            'response_body': process_history.response_body,
        }
        return j

    def to_entity(self, doc: dict) -> ProcessHistory:
        return ProcessHistory(
            started_at=doc.get('started_at'),
            duration_seconds=doc.get('duration_seconds'),
            status_code=doc.get('status_code'),
            request_header=doc.get('request_header'),
            request_body=doc.get('request_body'),
            response_header=doc.get('response_header'),
            response_body=doc.get('response_body'),
        )


class DatastoreGumoTaskProcessMapper:
    @inject
    def __init__(
            self,
            entity_key_mapper: EntityKeyMapper,
            process_history_mapper: DatastoreGumoProcessHistoryMapper,
    ):
        self._entity_key_mapper = entity_key_mapper
        self._process_history_mapper = process_history_mapper

    def to_datastore_entity(self, task_process: GumoTaskProcess) -> DatastoreEntity:
        entity = DatastoreEntity(key=self._entity_key_mapper.to_datastore_key(entity_key=task_process.key))
        entity.update({
            'relative_uri': task_process.relative_uri,
            'method': task_process.method,
            'payload': task_process.payload,
            'schedule_time': task_process.schedule_time,
            'created_at': task_process.created_at,
            'updated_at': task_process.updated_at,
            'state': task_process.state.value,
            'attemtps': task_process.attempts,
            'last_run_at': task_process.last_run_at,
            'run_at': task_process.run_at,
            'failed_at': task_process.failed_at,
            'histories': [
                self._process_history_mapper.to_datastore_entity(history) for history in task_process.histories
            ],
        })
        return entity

    def to_entity(self, datastore_entity: DatastoreEntity) -> GumoTaskProcess:
        key = self._entity_key_mapper.to_entity_key(datastore_entity.key)
        return GumoTaskProcess(
            key=key,
            relative_uri=datastore_entity.get('relative_uri'),
            method=datastore_entity.get('method'),
            payload=datastore_entity.get('payload'),
            schedule_time=datastore_entity.get('schedule_time'),
            created_at=datastore_entity.get('created_at'),
            updated_at=datastore_entity.get('updated_at'),
            state=TaskState.get(datastore_entity.get('state')),
            attempts=datastore_entity.get('attempts'),
            last_run_at=datastore_entity.get('last_run_at'),
            run_at=datastore_entity.get('run_at'),
            failed_at=datastore_entity.get('failed_at'),
            histories=[
                self._process_history_mapper.to_entity(history) for history in datastore_entity.get('histories')
            ],
        )
