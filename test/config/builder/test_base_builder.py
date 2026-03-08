from config.builder.base_builder import merge_cli_env
from config.builder.base_builder import get_yaml_file
from config.builder.base_builder import set_if_path_exists
from config.builder.base_builder import apply_overrides
from config.builder.base_builder import ConfigBuilder


def test_merge_cli_env_cli_overrides_env():

    cli = {"log_level": "DEBUG"}
    env = {"log_level": "INFO"}

    result = merge_cli_env(cli, env)

    assert result["log_level"] == "DEBUG"


def test_merge_cli_env_ignore_none():

    cli = {"log_level": None}
    env = {"log_level": "INFO"}

    result = merge_cli_env(cli, env)

    assert result["log_level"] == "INFO"



def test_get_yaml_file_cli_priority(tmp_path):

    f = tmp_path / "cli.yaml"
    f.write_text("test")

    cli = {"yaml": str(f)}
    env = {}

    result = get_yaml_file(cli, env, "default.yaml")

    assert result == str(f)


def test_get_yaml_file_env_priority(tmp_path):

    f = tmp_path / "env.yaml"
    f.write_text("test")

    cli = {}
    env = {"yaml": str(f)}

    result = get_yaml_file(cli, env, "default.yaml")

    assert result == str(f)


def test_get_yaml_file_default():

    cli = {}
    env = {}

    result = get_yaml_file(cli, env, "default.yaml")

    assert result == "default.yaml"



def test_set_if_path_exists_success():

    data = {
        "logging": {
            "level": "INFO"
        }
    }

    result = set_if_path_exists(data, "logging.level", "DEBUG")

    assert result is True
    assert data["logging"]["level"] == "DEBUG"


def test_set_if_path_exists_missing_path():

    data = {
        "logging": {}
    }

    result = set_if_path_exists(data, "logging.level", "DEBUG")

    assert result is False



def test_apply_overrides():

    yaml_data = {
        "logging": {
            "level": "INFO"
        }
    }

    overrides = {
        "logging.level": "DEBUG"
    }

    result = apply_overrides(yaml_data, overrides)

    assert result["logging"]["level"] == "DEBUG"



def test_config_builder_build(mocker):

    cli = {}
    env = {}
    default_yaml = "config.yaml"

    fake_yaml_data = {"logging": {"level": "INFO"}}

    mocker.patch(
        "pitpal.config.builder.base_builder.YamlLoader.load",
        return_value=fake_yaml_data
    )

    mocker.patch(
        "pitpal.config.builder.base_builder.ConfigConvertor.config_from_dict",
        return_value="CONFIG_OBJECT"
    )

    builder = ConfigBuilder(cli, env, default_yaml)

    result = builder.build("SomeClass")

    assert result == "CONFIG_OBJECT"
