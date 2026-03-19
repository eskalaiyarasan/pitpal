import tempfile
from pathlib import Path

import yaml


def write_to_temp(data: dict, key):
    # Create a temporary file with .yaml extension
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".yaml", mode="w")
    data[key]["yaml"] = temp.name
    # Write dict as YAML
    yaml.dump(data, temp, default_flow_style=False)

    temp.close()
    return temp.name  # return path to temp file


class YamlLoader:
    @staticmethod
    def load(path: str) -> dict:
        p = Path(path)

        if not p.exists():
            raise FileNotFoundError(f"Config YAML not found: {path}")

        with open(p, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return data or {}
