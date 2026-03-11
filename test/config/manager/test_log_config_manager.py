import argparse
import pytest
from unittest.mock import patch, MagicMock

from config.manager.log_config_manager import LoggingConfigManager
from config.interface.logging_config_database import module_name
from config.interface.logging_config_database import PitpalLoggingConfig


def test_singleton_behavior():
    m1 = LoggingConfigManager()
    m2 = LoggingConfigManager()

    assert m1 is m2


def test_prefix_matches_module_name():
    manager = LoggingConfigManager()

    assert manager.prefix == module_name


def test_register_arguments():
    manager = LoggingConfigManager()

    parser = argparse.ArgumentParser()
    manager.register_arguments(parser)

    args = parser.parse_args([
        "--logging-level", "DEBUG",
        "--logging-file-path", "app.log"
    ])

    assert args.logging_level == "DEBUG"
    assert args.logging_file_path == "app.log"
    assert args.logging_yaml is None


def test_extract_arguments():
    manager = LoggingConfigManager()

    parser = argparse.ArgumentParser()
    manager.register_arguments(parser)

    args = parser.parse_args([
        "--logging-level", "INFO",
        "--logging-file-path", "log.txt"
    ])

    result = manager.extract_arguments(args)

    assert result["logging.level"] == "INFO"
    assert result["logging.file.path"] == "log.txt"


def test_extract_arguments_missing_attr():
    manager = LoggingConfigManager()

    class DummyArgs:
        pass

    with pytest.raises(AttributeError):
        manager.extract_arguments(DummyArgs())

@patch("config.manager.log_config_manager.bb.ConfigBuilder")
@patch("config.manager.log_config_manager.el.get_env")
def test_get_config(mock_get_env, mock_builder):
    
    manager = LoggingConfigManager()

    # mock env variables
    mock_get_env.return_value = {"logging.level": "INFO"}

    # mock builder instance
    mock_builder_instance = MagicMock()
    mock_builder.return_value = mock_builder_instance

    # mock build() return
    expected_config = MagicMock(spec=PitpalLoggingConfig)
    mock_builder_instance.build.return_value = expected_config

    cli_args = {"logging.level": "DEBUG"}

    result = manager.get_config(cli_args)

    # assertions
    mock_get_env.assert_called_once_with(manager.prefix)

    mock_builder.assert_called_once_with(
        cli_args,
        mock_get_env.return_value,
        "config/default/logconfig.yaml"
    )
