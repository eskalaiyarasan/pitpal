import os
import yaml
from typing import Dict, Any, Optional


class ConfigBuilder:
    def __init__(
        self,
        yaml_path: Optional[str] = None,
        cli_args: Optional[Dict[str, Any]] = None,
    ):
        self.yaml_path = yaml_path
        self.cli_args = cli_args or {}

    def build(self) -> Dict[str, Any]:
        yaml_config = self._load_yaml()
        env_config = self._load_env()
        default_config = self._defaults()

        final = self._merge(
            default_config,
            yaml_config,
            env_config,
            self.cli_args,
        )

        return final

    def _load_yaml(self):
        if not self.yaml_path:
            return {}

        with open(self.yaml_path) as f:
            return yaml.safe_load(f) or {}

    def _load_env(self):
        return {
            "logging": {
                "level": os.getenv("PITPAL_LOG_LEVEL"),
                "file": os.getenv("PITPAL_LOG_FILE"),
            }
        }

    def _defaults(self):
        return {
            "logging": {
                "level": "INFO",
                "file": "logs/pitpal.log",
                "max_bytes": 1_000_000,
                "backup_count": 3,
            }
        }

    def _merge(self, *configs):
        result = {}
        for cfg in configs:
            result = self._deep_update(result, cfg)
        return result

    def _deep_update(self, base, new):
        for k, v in new.items():
            if isinstance(v, dict):
                base[k] = self._deep_update(base.get(k, {}), v)
            elif v is not None:
                base[k] = v
        return base
