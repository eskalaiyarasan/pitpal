import pytest
from config.builder.config_convertor import ConfigConvertor
from config.interface.logging_config_database import (
    PitpalLoggingConfig,
    LoggingConfig,
    ConsoleLoggingConfig,
    FileLoggingConfig,
    FormatConfig,
    RemoteLoggingConfig,
    SizeRotationConfig,
    TimeRotationConfig
)


def test_config_from_dict_basic():

    data = {
        "logging": {
            "level": "DEBUG",
            "console": {"enabled": True},
            "file": {
                "enabled": True,
                "path": "test.log",
                "rotate": "size",
                "size_rotation": {
                    "max_bytes": 1000,
                    "backup_count": 2
                },
                "time_rotation": {
                    "when": "midnight",
                    "interval": 1,
                    "backup_count": 7
                }
            },
            "format": {
                "style": "%",
                "pattern": "%(message)s"
            },
            "remote": {
                "enabled": False,
                "type": "http",
                "url": "http://localhost",
                "timeout": 5
            }
        }
    }

    result = ConfigConvertor.config_from_dict(PitpalLoggingConfig, data)

    assert isinstance(result, PitpalLoggingConfig)
    assert result.logging.level == "DEBUG"

def test_nested_dataclass_conversion():

    data = {
        "logging": {
            "level": "INFO",
            "console": {"enabled": True},
            "file": {
                "enabled": True,
                "path": "log.txt",
                "rotate": "size",
                "size_rotation": {
                    "max_bytes": 2000,
                    "backup_count": 3
                },
                "time_rotation": {
                    "when": "midnight",
                    "interval": 1,
                    "backup_count": 5
                }
            },
            "format": {"style": "%", "pattern": "%(message)s"},
            "remote": {
                "enabled": False,
                "type": "http",
                "url": "http://localhost",
                "timeout": 10
            }
        }
    }

    config = ConfigConvertor.config_from_dict(PitpalLoggingConfig, data)

    assert isinstance(config.logging.file, FileLoggingConfig)
    assert isinstance(config.logging.file.size_rotation, SizeRotationConfig)


def test_values_correctly_mapped():

    data = {
        "logging": {
            "level": "WARNING",
            "console": {"enabled": False},
            "file": {
                "enabled": True,
                "path": "app.log",
                "rotate": "size",
                "size_rotation": {
                    "max_bytes": 5000,
                    "backup_count": 4
                },
                "time_rotation": {
                    "when": "midnight",
                    "interval": 1,
                    "backup_count": 7
                }
            },
            "format": {"style": "%", "pattern": "%(levelname)s"},
            "remote": {
                "enabled": True,
                "type": "http",
                "url": "http://logserver",
                "timeout": 3
            }
        }
    }

    config = ConfigConvertor.config_from_dict(PitpalLoggingConfig, data)

    assert config.logging.file.path == "app.log"
    assert config.logging.file.size_rotation.max_bytes == 5000
    assert config.logging.remote.enabled is True


def test_missing_fields_become_none():

    data = {
        "logging": {
            "level": "INFO"
        }
    }

    config = ConfigConvertor.config_from_dict(PitpalLoggingConfig, data)

    assert config.logging.console is None
    assert config.logging.file is None
    assert config.logging.format is None
