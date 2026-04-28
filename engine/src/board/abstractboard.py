# boards are not register to any events.
# however boards can emit events
from abc import ABC, abstractmethod
from enum import Enum
import config.interface.rule_config_database as rm
import json

class State(Enum):
    NEW = 1
    READY = 2
    ERR = 3
    RUN = 4
    PAUSE = 5
    BLOCK = 6
    STOP = 7
    GAMEOVER = 8
    UNKNOWN = 0

def _set_param(data , value):
    typee=None
    if "Type" in data:
        typee = data["Type"]
     
    config = data["Param"]["Config"].strip()
    if config == "fixed":
        return False
    elif config == "flexi":
        if str(value) not in data["Param"]["Options"]:
            return False
    elif config == "user":
        pass
    else:
        return False
    
    data["Param"]["Enabled"] = True
    data["Param"]["Value"] = str(value)
    if typee == "enum":
        data["SubType"] = str(value)
    return True
    

class baseboard:
    def __init__(self):
        self.state = State.NEW

    @abstractmethod
    def move(self, index):
        if self.state != State.RUN:
            return False
        return [True, 0]

    def isGameOver(self):
        if self.state == State.GAMEOVER:
            return True
        return False

    @abstractmethod
    def repr(self):
        pass

    @abstractmethod
    def get_json(self):
        pass

    @classmethod
    def get_json(cls, config: rm.PitpalRuleConfig):
        if config.engine.algo.strip() != "classic":
            return None
        fp = open("engine/rules/classic.json", "r")
        json_data = json.load(fp)
        fp.close()
        if config.engine.details.time.enabled:
            pass #TimePerMove - work not started
        _set_param( json_data["pitsPerSide"] , config.engine.details.base.npits)
        _set_param( json_data["nSeeds"] , config.engine.details.base.nseeds)
        _set_param( json_data["nSide"] , config.engine.details.base.nside)
        return json_data
        


    
