# factory.py
from .engines import (
    ClassicProEngine,
    ClassicPodEngine,
    ClassicPalEngine
)

class EngineFactory:

    REGISTRY = {
        ("classic", "pro"): ClassicProEngine,
        ("classic", "pod"): ClassicPodEngine,
        ("classic", "pal"): ClassicPalEngine,
    }

    @classmethod
    def create_engine(cls, config):
        algo = config.get("algo", "classic")
        capture = config.get("capture", "pro")

        key = (algo, capture)

        engine_cls = cls.REGISTRY.get(key)

        if not engine_cls:
            raise ValueError(f"Unsupported engine combination: {key}")

        return engine_cls(config)
