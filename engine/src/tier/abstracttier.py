# tiers is the top most all the direct interaction called from here.
# from here,
#   config from db convert to json.
#   it will frame the necessary json merge to form final rules json 
#   the final rules json will follow the schema pal.rules.schema.json


from abc import ABC, abstractmethod
from enum import Enum

import utils.logging.pitpal_logger as pl
import engine.src.mode.mode as mode
import engine.src.board.board as board
import config.builder.base_builder as build
import json
import os

class basetier:
    def __init__(self):
        self.logger = pl.PitPalLogger.get_logger()
        self.jsonf=""

    @abstractmethod
    def init(self, config):
        if os.path.exists(self.jsonf):
            fp = open(self.jsonf,"r")
            self.json_data = json.load(fp)
            fp.close()
        try: 
            self.mode = mode.init_mode(config)
            self.board = board.init_board(config)
            return build.deep_merge(self.mode.get_json() , self.board.get_config())
        except Exception as e:
            self.logger.fatal(f"Failed: create engine: {e}")
            return None
        

    


