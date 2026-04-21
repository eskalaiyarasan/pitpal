from dataclasses import dataclass
from typing import Literal, Union


@dataclass(frozen=True)
class CloudEventConfig:
    url: str
    auth: str
    type: Literal["cloud"] = "cloud"


@dataclass(frozen=True)
class RemoteEventConfig:
    ip: str
    port: int
    auth: str
    type: Literal["remote"] = "remote"


@dataclass(frozen=True)
class LocalEventConfig:
    path: str
    auth: str
    type: Literal["local"] = "local"


# This represents the 'single' case without needing a full class
@dataclass(frozen=True)
class SingleEventConfig:
    enabled: bool = True
    type: Literal["single"] = "single"


# Define the Union: The 'param' can ONLY be one of these
EventParam = Union[
    SingleEventConfig, LocalEventConfig, RemoteEventConfig, CloudEventConfig
]


@dataclass(frozen=True)
class EventConfig:
    level: str
    param: EventParam  # This enforces that only ONE config type is passed
    yaml: str


@dataclass(frozen=True)
class PitpalEventConfig:
    event: EventConfig


module_name = "event"
