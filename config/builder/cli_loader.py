
import argparse

def register_arguments(parser, arglist: list):
    for opt in arglist:
        parser.add_argument(opt, default=None)

def extract_arguments(args, prefix, keys):
    result = {}

    for key in keys:
        key = key.lstrip("--")
        attr = key.replace("-", "_")

        if not hasattr(args, attr):
            raise AttributeError(f"Argument '{attr}' not found in args")

        path = key.replace("-", ".")
        result[path] = getattr(args, attr)

    return result
