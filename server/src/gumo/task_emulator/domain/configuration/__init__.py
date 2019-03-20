import dataclasses


@dataclasses.dataclass(frozen=True)
class TaskEmulatorConfiguration:
    server_host: str
