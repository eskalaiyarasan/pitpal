import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Dict, Any
import yaml


class PitPalLogger:
    """
    Singleton logger for PitPal.

    Usage:
        PitPalLogger.initialize(...)
        logger = PitPalLogger.get_logger()
    """

    _initialized = False
    _logger: Optional[logging.Logger] = None

    @classmethod
    def initialize(
        cls,
        yaml_path: Optional[str] = None,
        cli_args: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize logging system.
        Safe to call multiple times (only first call applies).
        """
        if cls._initialized:
            return

        cli_args = cli_args or {}
        yaml_config = cls._load_yaml(yaml_path)
        env_config = cls._load_env()

        def resolve(key: str, default=None):
            # Priority: CLI > ENV > YAML > Default
            if key in cli_args and cli_args[key] is not None:
                return cli_args[key]
            if env_config.get(key):
                return env_config[key]
            if key in yaml_config:
                return yaml_config[key]
            return default

        level_str = resolve("level", "INFO")
        log_file = resolve("file", "logs/pitpal.log")
        max_bytes = resolve("max_bytes", 1_000_000)
        backup_count = resolve("backup_count", 3)

        level = getattr(logging, level_str.upper(), logging.INFO)

        Path(log_file).parent.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger("pitpal")
        logger.setLevel(level)
        logger.handlers.clear()
        logger.propagate = False

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        # Console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Rotating file
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=int(max_bytes),
            backupCount=int(backup_count),
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        cls._logger = logger
        cls._initialized = True

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if not cls._initialized:
            raise RuntimeError("PitPalLogger not initialized. Call initialize() first.")
        return cls._logger

    @classmethod
    def reset(cls):
        """
        ONLY for testing.
        Clears singleton state.
        """
        if cls._logger:
            for handler in cls._logger.handlers:
                handler.close()
            cls._logger.handlers.clear()

        cls._logger = None
        cls._initialized = False

    @staticmethod
    def _load_yaml(path: Optional[str]) -> Dict[str, Any]:
        if not path:
            return {}
        with open(path, "r") as f:
            data = yaml.safe_load(f) or {}
        return data.get("logging", {})

    @staticmethod
    def _load_env() -> Dict[str, Any]:
        return {
            "level": os.getenv("PITPAL_LOG_LEVEL"),
            "file": os.getenv("PITPAL_LOG_FILE"),
            "max_bytes": os.getenv("PITPAL_LOG_MAX_BYTES"),
            "backup_count": os.getenv("PITPAL_LOG_BACKUP_COUNT"),
        }
