#!/usr/bin/env python3
# Copyright (C) 2026 Pitpal
#
# This file is part of PitPal.
#
# PitPal is free software: you can redistribute it and/or modify
# stickly not use for commericial purposes.#
# PitPal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
#    Author    :  Kalaiyarasan Es
#    File name :  pitpal/engine/src/engine.py
#    Date      :  02/03/2026
#######################################################################

from config.interface.rule_config_database  import *
from utils.oops.singleton import Singleton
from utils.jsonUtils.pitpal_json_schema_utils import JSU
import os
import json


class RuleNotFoundError(Exception):
    pass

class RuleNotValidError(Exception):
    pass


class PitpalEngine(Singleton):
    def __init__(self, config : PitpalRuleConfig):
        self.config = config
        self.default ={ "schema": "engine/rules/schema/pal.rules.schema.json"}
        jsonfile=config.engine.rule.json
        if jsonfile is None or jsonfile.strip() = "":
            self.make_custom()
        elif not os.path.exists(jsonfile):
            raise RuleNotFoundError(f"{jsonfile} rule not found")
        else:
            jsondata={}
            with open(jsonfile, "r") as file:
                jsondata=json.load(file)
            jsu=JSU(self.default["schema"] , jsondata)
            if jsu.validate():
                pass
            else:
                raise RuleNotValidError(f"{jsondata} rule not valid")

    def make_custom(self):
        pass  #not in the current scope. for future




