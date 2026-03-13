
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from typing import Optional

from config.interface.logging_config_database import PitpalLoggingConfig


class PitPalLogger:
    """
    Singleton logger for PitPal.

    Usage:
        PitPalLogger.initialize(config)
        logger = PitPalLogger.get_logger()
    """

    _initialized = False
    _logger: Optional[logging.Logger] = None

    @classmethod
    def initialize(cls, config: PitpalLoggingConfig) -> None:
        """
        Initialize logging using PitpalLoggingConfig object.
        Safe to call multiple times.
        """
        if cls._initialized:
            return

        log_cfg = config.logging

        level = getattr(logging, log_cfg.level.upper(), logging.INFO)

        logger = logging.getLogger("pitpal")
        logger.setLevel(level)
        logger.handlers.clear()
        logger.propagate = False

        # formatter
        style=str(log_cfg.format.style)
        if style == "text":
            style = "%"
        elif style == "json":
            style = "{"
        else:
            raise ValueError(f"Invalid log formatter style: {style}")
        formatter = logging.Formatter(
            log_cfg.format.pattern,
            style=style,
        )

        # ----------------------
        # Console logging
        # ----------------------
        if log_cfg.console.enabled:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        # ----------------------
        # File logging
        # ----------------------
        if log_cfg.file.enabled:
            file_cfg = log_cfg.file

            Path(file_cfg.path).parent.mkdir(parents=True, exist_ok=True)

            if file_cfg.rotate == "size":
                handler = RotatingFileHandler(
                    file_cfg.path,
                    maxBytes=int(file_cfg.sizerotation.max) *1024,
                    backupCount=file_cfg.sizerotation.backupcount,
                )

            elif file_cfg.rotate == "time":
                handler = TimedRotatingFileHandler(
                    file_cfg.path,
                    when=file_cfg.timerotation.when,
                    interval=file_cfg.timerotation.interval,
                    backupCount=file_cfg.timerotation.backupcount,
                )

            else:
                handler = logging.FileHandler(file_cfg.path)

            handler.setFormatter(formatter)
            logger.addHandler(handler)

        cls._logger = logger
        cls._initialized = True

        logger.info("PitPal logger initialized")

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
