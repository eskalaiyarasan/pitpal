from dataclasses import dataclass
from config.builder.cli_manager as manager
from utils.oops.singleton import Singleton

class LogginConfigManager(Singleton):

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.args=["--log-level","--log-file","--log-yaml"]
            self._initialized = True

    def register_logger_arguments(self, parser):
        return manager.register_arguments(parser, self.args)
    
    def  extract_logger_arguments(self,arg):
        return manager.extract_arguments(arg,self.args)


@dataclass(frozen=True)
class SizeRotationConfig:
    max_bytes: int
    backup_count: int


@dataclass(frozen=True)
class TimeRotationConfig:
    when: str
    interval: int
    backup_count: int


@dataclass(frozen=True)
class FileLoggingConfig:
    enabled: bool
    path: str
    rotate: str
    size_rotation: SizeRotationConfig
    time_rotation: TimeRotationConfig


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

@dataclass(frozen=True)
class PitpalLoggingConfig:
    logging: LoggingConfig
