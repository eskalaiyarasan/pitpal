import pytest
import tempfile
from pathlib import Path
from config.builder.yaml_loader import YamlLoader


def test_yaml_loader_success():
    path="./config/default/logconfig.yaml"
    data = YamlLoader.load(path)

    assert data["logging"]["level"] == "INFO"
    assert data["logging"]["file"]["enabled"]  == True


def test_yaml_loader_empty_yaml():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("")
        path = f.name

    data = YamlLoader.load(path)

    assert data == {}


def test_yaml_loader_file_not_found():
    with pytest.raises(FileNotFoundError):
        YamlLoader.load("non_existing.yaml")
