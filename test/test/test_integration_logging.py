import argparse
import pytest

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
    yaml_file.write_text(f"""
logging:
  level: {yaml_level}
""")

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

@pytest.mark.parametrize(
    "rotate_type, rotate_size, rotate_time",
    [
        ("size", "10MB", None),
        ("time", None, "midnight"),
    ],
)
def test_rotation_modes(tmp_path, rotate_type, rotate_size, rotate_time):

    yaml_file = tmp_path / "log.yaml"
    yaml_file.write_text("""
logging:
  level: INFO
""")

    manager = LoggingConfigManager()

    parser = argparse.ArgumentParser()
    manager.register_arguments(parser)

    args_list = ["--logging-yaml", str(yaml_file),
                 "--logging-rotate-type", rotate_type]

    if rotate_size:
        args_list += ["--logging-rotate-size", rotate_size]

    if rotate_time:
        args_list += ["--logging-rotate-time", rotate_time]

    args = parser.parse_args(args_list)

    cli_dict = manager.extract_arguments(args)

    config = manager.get_config(cli_dict)

    assert config.logging.rotate.type == rotate_type

