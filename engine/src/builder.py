# builder.py
from .factory import EngineFactory
from .decorators import (
    ModDecorator,
    CaptureDecorator,
    KingzpitDecorator
)

from config.interface.rule_config_database  import *
from utils.oops.singleton import Singleton
from utils.jsonUtils.pitpal_json_schema_utils import JSU
import os
import json


class RuleNotFoundError(Exception):
    pass

class RuleNotValidError(Exception):
    pass






class EngineBuilder:

    DECORATORS = {
        "engine.board.fruit": ModDecorator,
        "engine.board.captureplus": CaptureDecorator,
        "engine.rule.kingzpit": KingzpitDecorator,
        "engine.board.time": TimeDecorator,
        "engine.board.clock": ClockDecorator
    }
    
    def make_custom(self):
        pass  #not in the current scope. for future

    @classmethod
    def build(cls, config):
        #Pre-condition check 
        default ={ "schema": "engine/rules/schema/pal.rules.schema.json",
                  "deco": ["engine.board.fruit", "engine.board.time" , "engine.board.clock", "engine.board.captureplusn"
                           "engine.rule.kingzpit"]}
        jsonfile=config.engine.rule.json
        engine=None
        jsu=None
        if jsonfile is None or jsonfile.strip() = "":
            cls.make_custom()
        elif not os.path.exists(jsonfile):
            raise RuleNotFoundError(f"{jsonfile} rule not found")
        else:
            jsondata={}
            with open(jsonfile, "r") as file:
                jsondata=json.load(file)
            jsu=JSU(self.default["schema"] , jsondata)
            if jsu.validate():
                capture = jsu[""]
                engine = EngineFactory.create_engine(config)
            else:
                raise RuleNotValidError(f"{jsondata} rule not valid")
        if engine == None or jsu == None:
            raise RuleNotFoundError(f" not matching rule found")
        decorators = []
        for x in default["deco"]:
            attr=config
            y=x.split(".")
            for y in x.xplit("."):
                attr = getattr(attr,y)
            decorators.append(attr)

        for deco in decorators:
            deco_cls = cls.DECORATORS.get(deco)
            if deco_cls:
                engine = deco_cls(engine)

        return engine
