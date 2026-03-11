import os

PREFIX = "PITPAL_"

def get_env(prefix: str) -> dict:
    result = {}

    env_prefix = PREFIX + prefix.upper() + "_"

    for key, value in os.environ.items():

        if not key.startswith(env_prefix):
            continue

        path = prefix + "." + key[len(env_prefix):].lower().replace("_", ".")
        result[path] = value

    return result
