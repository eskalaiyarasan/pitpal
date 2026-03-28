# classengines.py
from .base import PitpalEngine

class ClassicEngine(PitpalEngine):
    def __init__(self, capture):
        super().__init__(capture)

    def run(self):
        return "Running Classic Pro Engine"


class SilverEngine(PitpalEngine):
    def __init__(self, capture):
        super().__init__(capture)
    def run(self):
        return "Running Classic Pod Engine"


class SnakeEngine(PitpalEngine):
    def __init__(self, capture):
        super().__init__(capture)
    def run(self):
        return "Running Classic Pal Engine"

