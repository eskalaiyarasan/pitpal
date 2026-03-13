from dataclasses import dataclass

module_name="logging"

@dataclass(frozen=True)
class SizeRotationConfig:
    max: int
    backupcount: int


@dataclass(frozen=True)
class TimeRotationConfig:
    when: str
    interval: int
    backupcount: int


@dataclass(frozen=True)
class FileLoggingConfig:
    enabled: bool
    path: str
    rotate: str
    sizerotation: SizeRotationConfig
    timerotation: TimeRotationConfig


@dataclass(frozen=True)
class ConsoleLoggingConfig:
    enabled: bool


@dataclass(frozen=True)
class FormatConfig:
    style: str
    pattern: str


@dataclass(frozen=True)
class RemoteLoggingConfig:
    enabled: bool
    type: str
    url: str
    timeout: int


@dataclass(frozen=True)
class LoggingConfig:
    level: str
    console: ConsoleLoggingConfig
    file: FileLoggingConfig
    format: FormatConfig
    remote: RemoteLoggingConfig
    yaml: str

@dataclass(frozen=True)
class PitpalLoggingConfig:
    logging: LoggingConfig
