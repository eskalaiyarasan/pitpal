# base.py
from abc import ABC, abstractmethod

class BaseEngine(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def run(self):
        pass
