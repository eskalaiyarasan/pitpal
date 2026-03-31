from dataclasses import dataclass, fields
from typing import Optional


@dataclass(frozen=True)
class CloudEventConfig:
    enable: bool
    url: str  # Fixed: changed int to str for URL
    auth: str


@dataclass(frozen=True)
class RemoteEventConfig:
    enable: bool  # Fixed: changed int to bool
    ip: str
    port: int
    auth: str


@dataclass(frozen=True)
class LocalEventConfig:
    enable: bool
    path: str


@dataclass(frozen=True)
class EventParamConfig:
    # Use Optional and default to None
    single: Optional[bool] = None
    local: Optional[LocalEventConfig] = None
    remote: Optional[RemoteEventConfig] = None
    cloud: Optional[CloudEventConfig] = None

    def __post_init__(self):
        # Count how many fields are NOT None
        active_configs = [
            self.single is not None,
            self.local is not None,
            self.remote is not None,
            self.cloud is not None,
        ]

        count = sum(active_configs)

        if count == 0:
            raise ValueError("At least one configuration must be provided.")
        if count > 1:
            raise ValueError(
                "Only one of [single, local, remote, cloud] can be set at a time."
            )


@dataclass(frozen=True)
class EventConfig:
    level: str
    param: EventParamConfig  # Fixed name to match EventParamConfig
    yaml: str


@dataclass(frozen=True)
class PitpalEventConfig:
    engine: EventConfig


module_name = "event"
