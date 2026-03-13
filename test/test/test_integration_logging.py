import argparse
import pytest
import yaml

from config.manager.log_config_manager import LoggingConfigManager


@pytest.mark.parametrize(
    "yaml_level, env_level, cli_level, expected",
    [
        ("INFO", None, None, "INFO"),        # YAML only
        ("INFO", "WARNING", None, "WARNING"), # ENV overrides YAML
        ("INFO", "WARNING", "DEBUG", "DEBUG"), # CLI overrides ENV
        ("INFO", None, "ERROR", "ERROR"),     # CLI overrides YAML
    ],
)
def test_config_priority(tmp_path, monkeypatch, yaml_level, env_level, cli_level, expected):

    # Create temporary YAML
    yaml_file = tmp_path / "log.yaml"
    source_file="./config/default/logconfig.yaml"
    with open(source_file, 'r') as file:
        # Use safe_load for security, especially with untrusted sources
        data = yaml.safe_load(file)
    data["logging"]["yaml"] = str(yaml_file)
    data["logging"]["level"] = yaml_level

    with open( str(yaml_file), 'w') as file:
        # Use default_flow_style=False for human-readable, block-style indentation
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)

    manager = LoggingConfigManager()

    parser = argparse.ArgumentParser()
    manager.register_arguments(parser)

    args_list = ["--logging-yaml", str(yaml_file)]

    if cli_level:
        args_list += ["--logging-level", cli_level]

    args = parser.parse_args(args_list)

    # ENV override
    if env_level:
        monkeypatch.setenv("PITPAL_LOGGING_LEVEL", env_level)

    cli_dict = manager.extract_arguments(args)

    config = manager.get_config(cli_dict)

    assert config.logging.level == expected


"""
@pytest.mark.parametrize(
    "rotate_type, rotate_size, rotate_time",
    [
        ("size", "10MB", None),
        ("time", None, "midnight"),
    ],
)
def test_rotation_modes(tmp_path, rotate_type, rotate_size, rotate_time):

    yaml_file = tmp_path / "log.yaml"
    source_file="./config/default/logconfig.yaml"
    with open(source_file, 'r') as file:
        # Use safe_load for security, especially with untrusted sources
        data = yaml.safe_load(file)
    data["logging"]["yaml"] = str(yaml_file)

    with open( str(yaml_file), 'w') as file:
        # Use default_flow_style=False for human-readable, block-style indentation
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)


    manager = LoggingConfigManager()

    parser = argparse.ArgumentParser()
    manager.register_arguments(parser)

    args_list = ["--logging-yaml", str(yaml_file),
                 "--logging-file-rotate", rotate_type]

    if rotate_size:
        args_list += ["--logging-file-sizerotation-max", rotate_size]

    if rotate_time:
        args_list += ["--logging-file-timerotate-when", rotate_time]

    args = parser.parse_args(args_list)

    cli_dict = manager.extract_arguments(args)

    config = manager.get_config(cli_dict)

    assert config.logging.rotate.type == rotate_type
    """
