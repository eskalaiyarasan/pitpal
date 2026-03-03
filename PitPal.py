import argparse
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

    # Initialize logger ONCE here
    PitPalLogger.initialize(
        yaml_path=args.config,
        cli_args={
            "level": args.log_level,
            "file": args.log_file,
        },
    )

    engine = Engine()
    engine.run()


if __name__ == "__main__":
    main()
