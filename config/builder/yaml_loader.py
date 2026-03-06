
import yaml
from pathlib import Path


class YamlLoader:

    @staticmethod
    def load(path: str) -> dict:
        p = Path(path)

        if not p.exists():
            raise FileNotFoundError(f"Config YAML not found: {path}")

        with open(p, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return data or {}

