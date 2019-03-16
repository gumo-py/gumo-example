import dataclasses
from typing import List


@dataclasses.dataclass(frozen=True)
class _EntityKeyPair:
    kind: str
    name: str


@dataclasses.dataclass(frozen=True)
class EntityKey:
    pairs: List[_EntityKeyPair]


class EntityKeyFactory:
    def __init__(self):
        pass

    def build(self) -> EntityKey:
        pass
