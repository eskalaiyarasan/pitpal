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
#run the cli from base path
./kit/generator/python rules_cli.py \
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

from pathlib import Path


JSON_TYPE_MAP = {
    "string": str,
    "number": float,
    "integer": int,
    "boolean": bool,
    "array": list,
    "object": dict,
    "null": type(None),
}


class SchemaTypeResolver:
    def __init__(self, schema_path: str):
        self.schema={}
        self._load_schema(schema_path)

    # ---------------------------
    # Path Parsing
    # ---------------------------
    def _load_schema(self, schema_path):
        directory, rootfilename = os.path.split(schema_path)
        for filename in os.listdir(directory):
            filename = os.path.join(directory,filename)
            if filename.endswith(".json"):
                with open(filename) as sf: 
                    self.schema[filename] = json.load(sf)
                if filename == schema_path:
                    self.schema["."] = self.schema[filename]

    def _parse_path(self, path: str):
        tokens = []
        parts = path.split(".")

        for part in parts:
            while True:
                match = re.match(r"([^\[]+)\[(\d+)\]", part)
                if match:
                    tokens.append(match.group(1))
                    tokens.append(int(match.group(2)))
                    part = part[match.end():]
                    if not part:
                        break
                else:
                    tokens.append(part)
                    break

        return tokens

    # ---------------------------
    # $ref Resolver
    # ---------------------------
    def _resolve_ref(self, ref: str):
        parts2 = ref.split("#/")
        parts = parts2[1].split("/")
        index=parts2[0].rstrip().lstrip()


        
        if index in self.schema:
                current = self.schema[index]
        else:
                raise KeyError(f"$ref path invalid: {ref}")

        for part in parts:
                if part not in current:
                    raise KeyError(f"$ref path invalid: {ref}")
                else:
                    current = current[part]

        return current

    def _fully_resolve(self, node):
        """
        Recursively resolve $ref chains.
        """
        if "$ref" in node:
            node = self._resolve_ref(node["$ref"])
        return node

    # ---------------------------
    # Extract Python Type
    # ---------------------------
    def _extract_type(self, node):
        node = self._fully_resolve(node)

        # Handle oneOf / anyOf
        if "oneOf" in node:
            return self._merge_types(node["oneOf"])

        if "anyOf" in node:
            return self._merge_types(node["anyOf"])

        if "type" in node:
            t = node["type"]

            if isinstance(t, list):
                return [JSON_TYPE_MAP[x] for x in t if x in JSON_TYPE_MAP]

            return JSON_TYPE_MAP.get(t)

        # If object without explicit type
        if "properties" in node:
            return dict

        return None

    def _merge_types(self, schemas):
        types = []
        for s in schemas:
            t = self._extract_type(s)
            if isinstance(t, list):
                types.extend(t)
            elif t:
                types.append(t)

        # remove duplicates
        return list(set(types))

    # ---------------------------
    # Public API
    # ---------------------------
    def get_type(self, path: str):
        tokens = self._parse_path(path)
        current = self.schema["."]

        for token in tokens:
            current = self._fully_resolve(current)

            if isinstance(token, str):
                if "properties" in current and token in current["properties"]:
                    current = current["properties"][token]
                else:
                    print(f"Property '{token}' not found in schema")
                    raise KeyError(f"Property '{token}' not found in schema")

            elif isinstance(token, int):
                # must be array
                resolved_type = self._extract_type(current)

                if resolved_type == list or (
                    isinstance(resolved_type, list) and list in resolved_type
                ):
                    current = current.get("items", {})
                else:
                    print(f"Property '{token}' not found in array")
                    raise TypeError(
                        f"Attempted array index on non-array type at '{token}'"
                    )

        return self._extract_type(current)



def load_schema(schema_path):
    directory, rootfilename = os.path.split(schema_path)
    registry = Registry()
    root_schema="{}"
    for filename in os.listdir(directory):
        filename = os.path.join(directory,filename)
        if filename.endswith(".json"):
            with open(filename) as sf:
                schema_data = json.load(sf)

            schema_id = schema_data.get("$id", filename)
            registry = registry.with_resource(
                schema_id,
                Resource.from_contents(schema_data)
            )

            if filename == schema_path:
                root_schema = schema_data 
    validator = Draft202012Validator(root_schema, registry=registry)
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

def set_element_in_array(t,data,key,value):
    match = re.match(r"(\w+)\[(\d+)\]", key)
    if t == bool:
        value = int(value)
    if match:
        name = match.group(1)
        index = int(match.group(2))
        if name not in data or  isinstance(data[name], list):
            return False
        if len(data[name] ) > index:
               data[name][index] = t(value)
               return true
        elif len(data[name]) == index:
               data[name].append(t(value))
               return True
    return False

def parse_frame_array_if(t,value):
    value = value.rstrip()
    value = value.lstrip()
    result=[]
    if value[0] == '[' and value[-1] == ']':
        value=value[1:-1].split(",")
        for v in value:
            if t == bool:
                v = int(v)
            result.append(t(v))
        return result


    return None


    
# ---------------------------------------------------
# JSON Utilities
# ---------------------------------------------------

def apply_set(resolver,data,  key_path, value):
    keys = key_path.split(".")
    t=None
    try:
        t = resolver.get_type(key_path)
        print("type",t)
        if isinstance(t,list):
            if list in t and value.rstrip().startswith('['):
                t = resolver.get_type(key_path +"[0]")
            elif type(None) in t and value == "null":
                t=type(None)
                value=None
            elif str in t:
                t = str
            elif list in t :
                key_path = key_path +"[0]"
                t = resolver.get_type(key_path)
    except:
        print("X error resolving ",key_path)
        sys.exit(1)
    current = data
    v1 = parse_frame_array_if(t,value) 
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

    if  not set_element_in_array(t , current,key[-1],value):
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
        resolver = SchemaTypeResolver(args.schema)
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
            apply_set(resolver,rule_data,key.strip(), value.strip())

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
