import os

PREFIX = "PITPAL_"
def get_env(prefix):
    result = {}
    prefix = PREFIX + prefix
    for key, value in os.environ.items():
        if not key.startswith(prefix):
                continue
        path = key[len(prefix):].lower().replace("_", ".")

        result[path] = value

    return result


