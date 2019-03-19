import dataclasses
import enum
import datetime

from typing import Optional
from typing import List

from gumo.datastore import EntityKey
from gumo.task.domain import GumoTask


class TaskState(enum.Enum):
    QUEUED = 'queued'
    PROCESSING = 'processing'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'

    def is_finished(self):
        return self == self.SUCCEEDED or self == self.FAILED

    def is_processing(self):
        return self == self.PROCESSING

    def is_queued(self):
        return self == self.QUEUED


@dataclasses.dataclass(frozen=True)
class ProcessHistory:
    started_at: datetime.datetime
    duration_seconds: int
    status_code: int
    request_header: str
    request_body: str
    response_header: str
    response_body: str


@dataclasses.dataclass(frozen=True)
class GumoTaskEmulator:
    KIND = 'GumoTaskEmulator'

    key: EntityKey
    state: TaskState = TaskState.QUEUED
    attempts: int = 0
    last_run_at: Optional[datetime.datetime] = None
    run_at: Optional[datetime.datetime] = None
    failed_at: Optional[datetime.datetime] = None
    histories: List[ProcessHistory] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        if self.key.parent().kind() != GumoTask.KIND:
            raise ValueError(f'key parent must be a GumoTask, but got: {self.key.key_literal()}')
