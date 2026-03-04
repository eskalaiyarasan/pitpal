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
        logging_config: dict) -> None:
        """
        Initialize logging system.
        Safe to call multiple times (only first call applies).
        """
        if cls._initialized:
            return

        level_str = logging_config["level"]
        log_file =  logging_config["file"]
        max_bytes =  logging_config["maxKB"]
        backup_count =  logging_config["nBackup"]


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

