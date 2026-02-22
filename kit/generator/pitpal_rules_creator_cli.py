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
#######################################################################
import json
import os
import argparse
import sys
import re
import ast
from copy import deepcopy
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

def load_schema(schema_path):
    curdir = os.getcwd()
    directory, filename = os.path.split(schema_path)
    os.chdir(directory)
    registry = Registry()
    for filename in os.listdir():
        if filename.endswith(".json"):
            with open(filename) as sf:
                schema_data = json.load(sf)

            schema_id = schema_data.get("$id", filename)

            registry = registry.with_resource(
                schema_id,
                Resource.from_contents(schema_data)
            )
    root_schema="{}"
    with open(filename) as f:
        root_schema = json.load(f)
    validator = Draft202012Validator(root_schema, registry=registry)
    os.chdir(curdir)
    return validator
def check_matching(validator,json_data):
    try:
        validator.validate(json_data)
        return True
    except:
        return False


def get_element_in_array(data,key):
    match = re.match(r"(\w+)\[(\d+)\]", key)
    if match:
        name = match.group(1)
        index = int(match.group(2))
        if name not in data or  isinstance(data[name], list):
            return None
        if len(data[name])  > index:
               return data[name][index] 
    return None

def set_element_in_array(data,key,value):
    match = re.match(r"(\w+)\[(\d+)\]", key)
    if match:
        name = match.group(1)
        index = int(match.group(2))
        if name not in data or  isinstance(data[name], list):
            return False
        if len(data[name] ) > index:
               t = type( data[name][index])
               data[name][index] = t(value)
               return true
        elif len(data[name]) == index:
               data[name].append(value)
               return True
    return False

def parse_frame_array_if(value):
    value = value.rstrip()
    value = value.lstrip()
    if value[0] == '[' and value[-1] == ']':
         return ast.literal_eval(value)
    return None


    
# ---------------------------------------------------
# JSON Utilities
# ---------------------------------------------------

def apply_set(data,  key_path, value):
    keys = key_path.split(".")
    current = data
    v1 = parse_frame_array_if(value) 
    if v1 != None:
        value = v1
    deco="  "
    for key in keys[:-1]:
        #print(deco+"key:",key)
        deco = deco+"  "
        k1 =get_element_in_array(current , key) 
        if k1 != None:
            current = k1
        elif key not in current:
            return
        else:
            current = current[key]
    if  not set_element_in_array(current,key[-1],value):
        t = type( current[keys[-1]] )
        if t == bool:
            value = int(value)
        current[keys[-1]] = t(value)
        #print(deco+"key:",keys[-1] ,t, t(value) , value)
    


def apply_unset(data, key_path):
    keys = key_path.split(".")
    current = data

    for key in keys[:-1]:
        if key not in current:
            return
        current = current[key]

    current.pop(keys[-1], None)
    return current


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
    if args.schema:
        validator = load_schema(args.schema)

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
            apply_set(rule_data,  key.strip(), value.strip())

    # Apply unset
    if args.unset:
        for key in args.unset:
            apply_unset(rule_data, key.strip())


    # Write output
    with open(args.output, "w") as f:
        json.dump(rule_data, f, indent=2)
    print("json rule generated successfully.")

    result = check_matching(validator , rule_data)

    if result:
        print("✅ Rule generated and Validated successfully.")
    else:
        print("X Rule Validation failed for the given Schema.")
    sys.exit(0)


if __name__ == "__main__":
    main()
