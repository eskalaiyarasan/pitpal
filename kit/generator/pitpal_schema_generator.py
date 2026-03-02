import argparse
import json
from pitpal_schema_service import JsonSchemaService
from pitpal_schema_json_mutator import (apply_set, apply_unset, deep_merge)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", required=True)
    parser.add_argument("--sample", required=True)
    parser.add_argument("--set", action="append")
    parser.add_argument("--unset", action="append")
    parser.add_argument("--patch")
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    engine = JsonSchemaService(args.schema)

    with open(args.sample) as f:
        data = json.load(f)

    if args.patch:
        with open(args.patch) as f:
            patch = json.load(f)
        deep_merge(data, patch)

    if args.set:
        for entry in args.set:
            key, value = entry.split("=", 1)
            apply_set(engine, data, key, value)

    if args.unset:
        for key in args.unset:
            apply_unset(data, key)

    engine.validate(data)

    with open(args.output, "w") as f:
        json.dump(data, f, indent=2)