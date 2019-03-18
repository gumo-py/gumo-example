import datetime
from typing import Optional

from gumo.datastore import EntityKey
from gumo.datastore import EntityKeyFactory

from gumo.task.domain import GumoTask


class GumoTaskFactory:
    def build(
            self,
            key: EntityKey,
            url: str,
            method: str = 'POST',
            payload: Optional[dict] = None,
            schedule_time: Optional[datetime.date] = None,
            in_seconds: Optional[int] = None,
            created_at: Optional[datetime.datetime] = None,
    ) -> GumoTask:
        now = datetime.datetime.utcnow().replace(microsecond=0)

        if schedule_time is not None and in_seconds is not None:
            raise ValueError('schedule_time and in_seconds should be specified exclusively.')

        if in_seconds:
            delta = datetime.timedelta(seconds=in_seconds)
            schedule_time = now + delta

        return GumoTask(
            key=key,
            url=url,
            method=method,
            payload=payload,
            schedule_time=schedule_time,
            created_at=created_at if created_at else now,
        )

    def build_for_new(
            self,
            url: str,
            method: str = 'POST',
            payload: Optional[dict] = None,
            schedule_time: Optional[datetime.date] = None,
            in_seconds: Optional[int] = None,
            created_at: Optional[datetime.datetime] = None,
    ) -> GumoTask:

        return self.build(
            key=EntityKeyFactory().build_for_new(kind=GumoTask.KIND),
            url=url,
            method=method,
            payload=payload,
            schedule_time=schedule_time,
            in_seconds=in_seconds,
            created_at=created_at,
        )
