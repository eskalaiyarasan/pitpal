import argparse
import glob
import os
import shutil
from pathlib import Path

import pytest

from config.manager.rules_config_manager import EngineConfigManager


@pytest.fixture
def engine_yaml_dir(logging_config, tmp_path):
    engine_dir = tmp_path / "config/system/engine"
    engine_dir.mkdir(parents=True)
    source_pattern = "config/system/engine/*.yaml"

    # Copy your uploaded YAMLs
    for file_path in glob.glob(source_pattern):
        shutil.copy(file_path, engine_dir)

    return engine_dir


@pytest.mark.parametrize(
    "env_level, cli_level, expected",
    [
        (None, None, "easy"),  # YAML only
        ("easy", None, "easy"),  # ENV overrides YAML
        ("easy", "hard", "hard"),  # CLI overrides ENV
        (None, "hard", "hard"),  # CLI overrides YAML
    ],
)
def test_config_priority(engine_yaml_dir, monkeypatch, env_level, cli_level, expected):
    ydir = engine_yaml_dir
    manager = EngineConfigManager()

    parser = argparse.ArgumentParser()
    manager.register_arguments(parser)
    args_list = ["--engine-dir", str(ydir)]
    args_list += ["--engine-rule", ": classic_pal"]
    if cli_level:
        args_list += ["--engine-level", cli_level]
    args = parser.parse_args(args_list)
    if env_level:
        monkeypatch.setenv("PITPAL_ENGINE_LEVEL", env_level)
    cli_dict = manager.extract_arguments(args)
    config = manager.get_config(cli_dict)
    assert config.engine.board.level == expected
