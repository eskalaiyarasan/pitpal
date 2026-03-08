import os
import logging
import pytest
from utils.logging.pitpal_logger import PitPalLogger




def setup_function():
    """
    Ensure singleton reset before each test
    """
    PitPalLogger.reset()


def test_initialize_creates_logger(logging_config):
    PitPalLogger.initialize(logging_config)

    logger = PitPalLogger.get_logger()

    assert isinstance(logger, logging.Logger)
    assert logger.name == "pitpal"


def test_initialize_creates_handlers(logging_config):
    PitPalLogger.initialize(logging_config)
    logger = PitPalLogger.get_logger()

    # console + file handler
    assert len(logger.handlers) == 2


def test_log_file_created(logging_config):
    PitPalLogger.initialize(logging_config)

    logger = PitPalLogger.get_logger()
    logger.info("test message")

    log_file = logging_config.logging.file.path

    if logging_config.logging.file.enabled:
        assert os.path.exists(log_file)
    else:
        assert not logging_config.logging.file.path


def test_singleton_initialize_only_once(logging_config):
    PitPalLogger.initialize(logging_config)
    logger1 = PitPalLogger.get_logger()

    # second initialize should not recreate
    PitPalLogger.initialize(logging_config)
    logger2 = PitPalLogger.get_logger()

    assert logger1 is logger2


def test_get_logger_without_initialize():
    with pytest.raises(RuntimeError):
        PitPalLogger.get_logger()


def test_reset_clears_logger(logging_config):
    PitPalLogger.initialize(logging_config)
    PitPalLogger.reset()

    with pytest.raises(RuntimeError):
        PitPalLogger.get_logger()

def test_no_duplicate_handlers(logging_config):

    PitPalLogger.initialize(logging_config)
    logger = PitPalLogger.get_logger()

    handlers_first = len(logger.handlers)

    PitPalLogger.initialize(logging_config)

    handlers_second = len(logger.handlers)

    assert handlers_first == handlers_second

def test_size_log_rotation(logging_config, tmp_path):
    """
    Verify size based rotation works.
    """

    # modify config for very small file size
    file_cfg = logging_config.logging.file
    object.__setattr__(file_cfg.size_rotation, "max_bytes", 200)
    object.__setattr__(file_cfg.size_rotation, "backup_count", 2)
    object.__setattr__(file_cfg, "rotate", "size")

    log_path = tmp_path / "size_rotation.log"
    object.__setattr__(file_cfg, "path", str(log_path))

    PitPalLogger.initialize(logging_config)
    logger = PitPalLogger.get_logger()

    # write enough logs to exceed 200 bytes
    for _ in range(50):
        logger.info("This is a log line to trigger size rotation")

    log_files = list(tmp_path.glob("size_rotation.log*"))

    # should create rotated file
    assert len(log_files) > 1

def test_time_log_rotation(logging_config, tmp_path):
    """
    Verify time based rotation works.
    """

    file_cfg = logging_config.logging.file

    object.__setattr__(file_cfg, "rotate", "time")
    object.__setattr__(file_cfg.time_rotation, "when", "S")
    object.__setattr__(file_cfg.time_rotation, "interval", 1)
    object.__setattr__(file_cfg.time_rotation, "backup_count", 2)

    log_path = tmp_path / "time_rotation.log"
    object.__setattr__(file_cfg, "path", str(log_path))

    PitPalLogger.initialize(logging_config)
    logger = PitPalLogger.get_logger()

    logger.info("before rotation")

    # force rollover
    handler = None
    for h in logger.handlers:
        if hasattr(h, "doRollover"):
            handler = h
            break

    assert handler is not None

    handler.doRollover()

    logger.info("after rotation")

    log_files = list(tmp_path.glob("time_rotation.log*"))

    assert len(log_files) > 1
