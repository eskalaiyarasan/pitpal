def deep_merge(base, patch):
    for key, value in patch.items():
        if isinstance(value, dict) and key in base:
            deep_merge(base[key], value)
        else:
            base[key] = value


def convert_value(t, value):
    if t == bool:
        return value.lower() in ("true", "1")
    if t == int:
        return int(value)
    if t == float:
        return float(value)
    if t == type(None):
        return None
    return t(value)


def apply_set(engine, data, key_path, value):
    keys = key_path.split(".")
    t = engine.get_type(key_path)

    current = data

    for key in keys[:-1]:
        current = current.setdefault(key, {})

    current[keys[-1]] = convert_value(t, value)


def apply_unset(data, key_path):
    keys = key_path.split(".")
    current = data

    for key in keys[:-1]:
        current = current[key]

    current.pop(keys[-1], None)