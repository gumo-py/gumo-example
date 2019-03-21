from injector import inject

from gumo.datastore import EntityKey
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
            process_history_mapper: DatastoreGumoProcessHistoryMapper,
    ):
        self._process_history_mapper = process_history_mapper

    def to_datastore_entity(self, task_process: GumoTaskProcess) -> dict:
        j = {
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
        }
        return j

    def to_entity(self, key: EntityKey, doc: dict) -> GumoTaskProcess:
        return GumoTaskProcess(
            key=key,
            relative_uri=doc.get('relative_uri'),
            method=doc.get('method'),
            payload=doc.get('payload'),
            schedule_time=doc.get('schedule_time'),
            created_at=doc.get('created_at'),
            updated_at=doc.get('updated_at'),
            state=TaskState.get(doc.get('state')),
            attempts=doc.get('attempts'),
            last_run_at=doc.get('last_run_at'),
            run_at=doc.get('run_at'),
            failed_at=doc.get('failed_at'),
            histories=[
                self._process_history_mapper.to_entity(history) for history in doc.get('histories')
            ],
        )
