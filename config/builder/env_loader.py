import os

PREFIX = "PITPAL_"
def get_env(prefix):
    result = {}
    prestr = PREFIX + prefix+"_"
    for key, value in os.environ.items():
        if not key.startswith(prestr):
                continue
        path = prefix+ "." + key[len(prestr):].lower().replace("_", ".")

        result[path] = value

    return result


