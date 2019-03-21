import dataclasses
import enum
import datetime

from typing import Optional
from typing import List

from gumo.datastore import EntityKey
from gumo.datastore import EntityKeyFactory
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

    @classmethod
    def get(cls, value: str):
        try:
            return cls(value)
        except ValueError:
            return cls.QUEUED


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
class GumoTaskProcess:
    KIND = 'GumoTaskProcess'

    key: EntityKey
    relative_uri: str
    method: str = 'POST'
    payload: Optional[dict] = dataclasses.field(default_factory=dict)
    schedule_time: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.utcnow)
    created_at: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.utcnow)
    state: TaskState = TaskState.QUEUED
    attempts: int = 0
    last_run_at: Optional[datetime.datetime] = None
    run_at: Optional[datetime.datetime] = None
    failed_at: Optional[datetime.datetime] = None
    histories: List[ProcessHistory] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        if self.key.kind() != self.KIND:
            raise ValueError(f'key KIND must be a {self.KIND}, but got: {self.key.kind()}')


class GumoTaskProcessFactory:
    def build_from_task(self, task: GumoTask) -> GumoTaskProcess:
        now = datetime.datetime.utcnow().replace(microsecond=0)

        return GumoTaskProcess(
            key=EntityKeyFactory().build(kind=GumoTaskProcess.KIND, name=task.key.name()),
            relative_uri=task.relative_uri,
            method=task.method,
            payload=task.payload,
            schedule_time=task.schedule_time,
            created_at=task.created_at,
            updated_at=now,
        )
