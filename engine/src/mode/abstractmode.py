# tiers will register to events pass to boards and viceversa.

from abc import ABC, abstractmethod
from enum import Enum

import utils.logging.pitpal_logger as pl


class basemode:
    def __init__(self):
        self.logger = pl.PitPalLogger.get_logger()

    @abstractmethod
    def init(self, config):
        pass
    @abstractmethod
    def get_json(self):
        pass
