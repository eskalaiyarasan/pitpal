import argparse
from config.config_builder import ConfigBuilder
from utils.logging.pitpal_logger import PitPalLogger
from engine.engine import Engine


def logging_args(parser):
    return {
            "level": args.log_level,
            "file": args.log_file,
            "cfg" : args.log_yaml,
        }

def argument_list():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level")
    parser.add_argument("--log-file")
    parser.add_argument("--log-yaml", default=None)
    return parser.parse_args()
def main():
    args = argument_list()
    log_config = logging_args(args)

    log_config = LogConfigBuilder(log_config).build()

    PitPalLogger.initialize(config["logging"])

    engine = Engine(config)
    engine.run()


if __name__ == "__main__":
    main()
