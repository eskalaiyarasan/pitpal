import argparse
from config.config_builder import ConfigBuilder
from utils.logging.pitpal_logger import PitPalLogger
from engine.engine import Engine


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level")
    parser.add_argument("--log-file")
    parser.add_argument("--config", default="config.yaml")
    return parser.parse_args()


def main():
    args = parse_args()

    cli_config = {
        "logging": {
            "level": args.log_level,
            "file": args.log_file,
        }
    }

    config = ConfigBuilder(
        yaml_path=args.config,
        cli_args=cli_config,
    ).build()

    PitPalLogger.initialize(config["logging"])

    engine = Engine(config)
    engine.run()


if __name__ == "__main__":
    main()
