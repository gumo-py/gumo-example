from injector import inject

from gumo.task_emulator.domain import GumoTaskProcess
from gumo.task_emulator.domain import ProcessHistory


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


class DatastoreGumoTaskProcessMapper:
    @inject
    def __init__(
            self,
            process_history_mapper: DatastoreGumoProcessHistoryMapper,
    ):
        self._process_history_mapper = process_history_mapper

    def to_datastore_entity(self, task_process: GumoTaskProcess) -> dict:
        j = {
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
