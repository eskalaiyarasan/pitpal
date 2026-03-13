import pytest
from config.interface.logging_config_database import (
    PitpalLoggingConfig,
    LoggingConfig,
    ConsoleLoggingConfig,
    FileLoggingConfig,
    FormatConfig,
    RemoteLoggingConfig,
    SizeRotationConfig,
    TimeRotationConfig
)


@pytest.fixture
def logging_config(tmp_path):
    log_file = tmp_path / "pitpal_test.log"

    config = PitpalLoggingConfig(
        logging=LoggingConfig(
            level="DEBUG",
            yaml="config/default/logconfig.yaml",

            console=ConsoleLoggingConfig(
                enabled=True
            ),

            file=FileLoggingConfig(
                enabled=True,
                path=str(log_file),
                rotate="size",

                sizerotation=SizeRotationConfig(
                    max_bytes= 100,
                    backupcount=3
                ),

                timerotation=TimeRotationConfig(
                    when="midnight",
                    interval=1,
                    backupcount=7
                )
            ),

            format=FormatConfig(
                style="%",
                pattern="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            ),

            remote=RemoteLoggingConfig(
                enabled=False,
                type="http",
                url="http://localhost",
                timeout=5
            )
        )
    )

    return config
