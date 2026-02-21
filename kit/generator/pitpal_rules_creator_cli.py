#!/usr/bin/env python3
# Copyright (C) 2026 Pitpal
#
# This file is part of PitPal.
#
# PitPal is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# either version 3 of the License, or (at your option) any later version.
#
# PitPal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PitPal. If not, see <https://www.gnu.org/licenses/>.
#    Author    :  Kalaiyarasan Es
#    File name :  pitpal/kit/generator/pitpal_rules_creator_cli.py
#    Date      :  21/02/2026
#######################################################################

import json
import os
import argparse
import sys
from copy import deepcopy
from jsonschema import Draft202012Validator
from referencing import Registry, Resource


"""
python rules_cli.py \
  --schema schemas/game.rule.schema.json \
  --sample rules/base.json \
  --set timeSupport.enabled=true \
  --set timeSupport.options=[10,20,30] \
  --unset debugMode \
  --patch override.json \
  --output rules/flexi.json
  --help
"""
# ---------------------------------------------------
# Schema Loader
# ---------------------------------------------------

def load_schema(schema_path):
    base_dir = os.path.dirname(schema_path)

    with open(schema_path, "r") as f:
        root_schema = json.load(f)

    registry = Registry()

    for filename in os.listdir(base_dir):
        if filename.endswith(".json"):
            full_path = os.path.join(base_dir, filename)
            with open(full_path, "r") as sf:
                schema_data = json.load(sf)

            schema_id = schema_data.get("$id", f"file://{full_path}")

            registry = registry.with_resource(
                schema_id,
                Resource.from_contents(schema_data)
            )

    validator = Draft202012Validator(root_schema, registry=registry)

    return root_schema, validator


# ---------------------------------------------------
# Schema Utilities
# ---------------------------------------------------

def get_schema_for_key(schema, key_path):
    keys = key_path.split(".")
    current = schema

    for key in keys:
        if "properties" in current and key in current["properties"]:
            current = current["properties"][key]
        else:
            return None

    return current


def convert_value_by_schema(value, schema):
    if "const" in schema:
        raise ValueError("Cannot modify const property")

    field_type = schema.get("type")

    if isinstance(field_type, list):
        field_type = [t for t in field_type if t != "null"][0]

    if field_type == "boolean":
        return value.lower() == "true"

    if field_type == "integer":
        return int(value)

    if field_type == "array":
        items_schema = schema.get("items", {})
        item_type = items_schema.get("type", "string")
        values = [v.strip() for v in value.split(",")]

        converted = []
        for v in values:
            if item_type == "integer":
                converted.append(int(v))
            elif item_type == "boolean":
                converted.append(v.lower() == "true")
            else:
                converted.append(v)
        return converted

    return value  # string default


# ---------------------------------------------------
# JSON Utilities
# ---------------------------------------------------

def apply_set(data, schema, key_path, value):
    schema_node = get_schema_for_key(schema, key_path)
    if not schema_node:
        raise ValueError(f"Invalid key: {key_path}")

    converted = convert_value_by_schema(value, schema_node)

    keys = key_path.split(".")
    current = data

    for key in keys[:-1]:
        current = current.setdefault(key, {})

    current[keys[-1]] = converted


def apply_unset(data, key_path):
    keys = key_path.split(".")
    current = data

    for key in keys[:-1]:
        if key not in current:
            return
        current = current[key]

    current.pop(keys[-1], None)


def deep_merge(base, patch):
    for key, value in patch.items():
        if isinstance(value, dict) and key in base:
            deep_merge(base[key], value)
        else:
            base[key] = value


# ---------------------------------------------------
# Main
# ---------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="PitPal Rules CLI Tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--schema", required=True,help="Path to root JSON schema file")
    parser.add_argument("--sample", required=True , help="Base rule JSON file")
    parser.add_argument("--set", action="append", help="Override value using dot notation (example: timeSupport.enabled=true)" )
    parser.add_argument("--unset", action="append",help="Remove property using dot notation (example: debugMode)" )
    parser.add_argument("--patch", help="Apply deep merge patch from JSON file")
    parser.add_argument("--output", required=True, help="Output file path")

    args = parser.parse_args()

    # Load sample
    with open(args.sample, "r") as f:
        rule_data = json.load(f)

    # Load schema
    schema, validator = load_schema(args.schema)

    # Apply patch
    if args.patch:
        with open(args.patch, "r") as f:
            patch_data = json.load(f)
        deep_merge(rule_data, patch_data)

    # Apply set
    if args.set:
        for entry in args.set:
            if "=" not in entry:
                print(f"Invalid format: {entry}")
                sys.exit(1)
            key, value = entry.split("=", 1)
            apply_set(rule_data, schema, key.strip(), value.strip())

    # Apply unset
    if args.unset:
        for key in args.unset:
            apply_unset(rule_data, key.strip())

    # Validate
    try:
        validator.validate(rule_data)
    except Exception as e:
        print("Validation failed:")
        print(e)
        sys.exit(1)

    # Write output
    with open(args.output, "w") as f:
        json.dump(rule_data, f, indent=2)

    print("✅ Rule generated successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()
