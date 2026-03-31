from dataclasses import dataclass

module_name = "engine"


@dataclass(frozen=True)
class CloudEventConfig:
    enable: bool
    url: int
    auth: str


@dataclass(frozen=True)
class RemoteEventConfig:
    enable: int
    ip: str
    port: int
    auth: str


@dataclass(frozen=True)
class LocalEventConfig:
    enable: bool
    path: str


@dataclass(frozen=True)
class EventParamConfig:
    single: bool
    local: LocalEventConfig
    remote: RemoteEventConfig
    cloud: CloudEventConfig


@dataclass(frozen=True)
class EventConfig:
    level: str
    param: EngineParamConfig
    yaml: str


@dataclass(frozen=True)
class PitpalEventConfig:
    engine: EventConfig
