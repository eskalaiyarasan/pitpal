from config.manager.config_manager import getLogConfigManager
from config.manager.log_config_manager import LoggingConfigManager


def test_get_log_config_manager():
    mgr = getLogConfigManager()

    assert isinstance(mgr, LoggingConfigManager)
