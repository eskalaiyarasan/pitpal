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
#    File name :  pitpal/utils/jsonItils/pitpal_json_schema_utils.py
#    Date      :  2/03/2026
#######################################################################

import json
import os
import sys
import re
import ast
from copy import deepcopy
from jsonschema import Draft202012Validator
from referencing import Registry, Resource


#JSU   : - JSON Schema Utility
class JSU:
    def __init__(self , schema_file: str , json_data ):
        self.schemaFile = schema_file
        self.schema = {}
        self.jsonData = json_data
        self._load_schema(schema_file)

    def _load_schema(self , schema_path):
        directory, rootfilename = os.path.split(schema_path)
        registry = Registry()
        for filename in os.listdir(directory):
            filename = os.path.join(directory, filename)
            if filename.endswith(".json"):
                schema_data=None
                with open(filename) as sf:
                    schema_data= json.load(sf)
                self.schema[filename] = schema_data;
                schema_id = schema_data.get("$id", filename)
                registry = registry.with_resource(
                    schema_id,
                    Resource.from_contents(schema_data)
                )
                if filename == schema_path:
                    self.schema["."] = self.schema[filename]
        self.validator = Draft202012Validator(self.schema["."], registry=registry)

    def validate(self):
        return self.validator(self.jsonData)



