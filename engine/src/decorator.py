# decorators.py
from .base import PitpalEngine

class EngineDecorator(PitpalEngine):
    def __init__(self, engine: PitpalEngine):
        self.engine = engine

    def run(self):
        return self.engine.run()


class ModDecorator(EngineDecorator):
    def run(self):
        result = self.engine.run()
        return f"[MOD] -> {result}"


class CaptureDecorator(EngineDecorator):
    def run(self):
        result = self.engine.run()
        return f"[CAPTURE] -> {result}"


class KingzpitDecorator(EngineDecorator):
    def run(self):
        result = self.engine.run()
        return f"[KINGZPIT] -> {result}"
