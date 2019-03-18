import dataclasses
import datetime

from typing import Optional

from gumo.datastore import EntityKey


@dataclasses.dataclass(frozen=True)
class GumoTask:
    KIND = 'GumoTask'

    key: EntityKey
    url: str
    method: str = 'POST'
    payload: Optional[dict] = dataclasses.field(default_factory=dict)
    schedule_time: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.utcnow)
    created_at: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.utcnow)