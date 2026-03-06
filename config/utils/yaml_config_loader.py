from dataclasses import fields, is_dataclass
from dataclasses import replace


def config_from_dict(dataclass_type, data: dict):
    """
    Recursively convert dict → dataclass
    """

    if not is_dataclass(dataclass_type):
        return data

    kwargs = {}

    for field in fields(dataclass_type):
        value = data.get(field.name) if data else None

        if value is None:
            kwargs[field.name] = None
            continue

        if is_dataclass(field.type):
            kwargs[field.name] = config_from_dict(field.type, value)
        else:
            kwargs[field.name] = value

    return dataclass_type(**kwargs)

def override_config(configs, args):
    for key,value in args.items():
            if value is None:
                continue
            configs = replace(configs, **{key: value})
    return configs
