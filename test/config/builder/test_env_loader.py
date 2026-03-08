from config.builder.env_loader import get_env


def test_env_loader_single_variable(monkeypatch):

    monkeypatch.setenv("PITPAL_LOGGING_LEVEL", "DEBUG")

    result = get_env("LOGGING")
    with open("debug.log", "w") as f:
        f.write(str(result))
    assert result["LOGGING.level"] == "DEBUG"

def test_env_loader_multiple_variables(monkeypatch):

    monkeypatch.setenv("PITPAL_LOGGING_LEVEL", "INFO")
    monkeypatch.setenv("PITPAL_LOGGING_FILE_PATH", "/tmp/app.log")

    result = get_env("LOGGING")

    assert result["LOGGING.level"] == "INFO"
    assert result["LOGGING.file.path"] == "/tmp/app.log"

def test_env_loader_ignore_other_variables(monkeypatch):

    monkeypatch.setenv("PITPAL_ENGINE_PORT", "9000")

    result = get_env("LOGGING")

    assert result == {}

def test_env_loader_empty(monkeypatch):

    monkeypatch.delenv("PITPAL_LOGGING_LEVEL", raising=False)

    result = get_env("LOGGING")

    assert result == {}
