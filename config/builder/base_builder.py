from config.builder.yaml_loader import YamlLoader
from config.builder.config_convertor import ConfigConvertor
import os

def merge_cli_env(cli_args: dict, env_vars: dict) -> dict:
    """
    Merge two flat dot-path dictionaries and convert to nested dict.
    dict1 overrides dict2.
    """
    dict1 = cli_args
    dict2 = env_vars

    merged = {}

    # dict2 first (lower priority)
    merged.update(dict2)

    # dict1 overrides
    merged.update(dict1)

    result = {}

    for path, value in merged.items():
        keys = path.split(".")
        cur = result

        for key in keys[:-1]:
            cur = cur.setdefault(key, {})

        cur[keys[-1]] = value

    return result


def get_yaml_file(cli_args, env_vars, default_yaml):
    if cli_args.get("yaml") and os.path.exists(cli_args.get("yaml")):
        return cli_args["yaml"]

    if env_vars.get("yaml") and os.path.exists(env_vars.get("yaml")):
        return env_vars["yaml"]

    return default_yaml

def set_if_path_exists(data: dict, path: str, value):
    keys = path.split(".")
    current = data

    for key in keys[:-1]:
        if key not in current:
            return False
        current = current[key]

    if keys[-1] in current:
        current[keys[-1]] = value
        return True

    return False

def apply_overrides(yaml_data: dict, overrides: dict):

    for key, value in overrides.items():
        set_if_path_exists(yaml_data, key, value)

    return yaml_data

class ConfigBuilder:

    def __init__(self, cli_args, env_vars, default_yaml):
        self.cli = cli_args
        self.env = env_vars
        self.default_yaml = default_yaml

    def build(self, cc):

        yaml_file = get_yaml_file(self.cli, self.env, self.default_yaml)

        yaml_data = YamlLoader.load(yaml_file)

        overrides = merge_cli_env(self.cli, self.env)

        final_data = apply_overrides(yaml_data, overrides)

        return ConfigConvertor.config_from_dict(cc,final_data)
