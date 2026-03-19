from config.builder.yaml_loader import YamlLoader
from config.builder.config_convertor import ConfigConvertor
import os

from collections.abc import Mapping
from copy import deepcopy


def deep_merge(A: dict, B: dict) -> dict:
    """
    Deep-merge dicts A and B into a new dict.
    [    - Recursively merges nested dicts.
    - When keys conflict, A's value takes precedence over B's.
    - Does not mutate A or B.
    """
    def _merge(a, b):
        # Start from a deep copy of b so we don't mutate inputs
        result = deepcopy(b)
        for k, a_val in a.items():
            if k in result:
                b_val = result[k]
                if isinstance(a_val, Mapping) and isinstance(b_val, Mapping):
                    result[k] = _merge(a_val, b_val)  # merge nested dicts
                else:
                    result[k] = deepcopy(a_val)       # A overrides B
            else:
                result[k] = deepcopy(a_val)           # add new key from A
        return result

    return _merge(A, B)

def merge(cli_args: dict, env_vars: dict) -> dict:
    result = env_vars.copy()

    for k, v in cli_args.items():
        if v is not None:
            result[k] = v

    return result

def xmerge_cli_env(cli_args: dict, env_vars: dict) -> dict:
    """
    Merge two flat dot-path dictionaries and convert to nested dict.
    dict1 overrides dict2.
    """
    dict_arr =[ env_vars , cli_args ]


    result = {}
    for x in dict_arr :
        for path, value in x.items():
            keys = path.split(".")
            cur = result
            if value == None:
                continue;

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

    if value is None:
        return False

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

    def __init__(self, cli_args, env_vars, default_yaml, order=None):
        self.cli = cli_args
        self.env = env_vars
        self.default_yaml = default_yaml
        self.order=order

    def build(self, cc):
        if self.order==None:
            return self.build_default(cc)
        else:
            pass

    def build_default(self, cc):

        yaml_file = get_yaml_file(self.cli, self.env, self.default_yaml)

        yaml_data = YamlLoader.load(yaml_file)

        overrides = merge(self.cli, self.env)

        final_data = apply_overrides(yaml_data, overrides)

        return ConfigConvertor.config_from_dict(cc,final_data)
