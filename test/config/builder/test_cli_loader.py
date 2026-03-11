import pytest
import argparse
from config.builder.cli_loader import register_arguments, extract_arguments


def test_register_arguments():
    parser = argparse.ArgumentParser()
    arglist = ["--log-level", "--log-file"]

    register_arguments(parser, arglist)

    args = parser.parse_args(["--log-level", "INFO"])

    assert args.log_level == "INFO"
    assert args.log_file is None


def test_extract_arguments_success():
    parser = argparse.ArgumentParser()

    parser.add_argument("--log-level")
    parser.add_argument("--log-file")

    args = parser.parse_args(["--log-level", "DEBUG", "--log-file", "app.log"])

    result = extract_arguments(
        args,
        "log",
        ["--log-level", "--log-file"]
    )

    assert result["log.level"] == "DEBUG"
    assert result["log.file"] == "app.log"


def test_extract_arguments_missing_attribute():
    class DummyArgs:
        pass

    args = DummyArgs()

    with pytest.raises(AttributeError):
        extract_arguments(args, "log", ["--log-level"])
