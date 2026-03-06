import argparse
from config.core.config_manager as CM
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
    CM.register_log_args(parser)
    return parser.parse_args()

def main():
    args = argument_list()
    log_config = CM.extract_logger_cli(args)

    log_config = LogConfigBuilder(log_config).build()

    PitPalLogger.initialize(config["logging"])

    engine = Engine(config)
    engine.run()


if __name__ == "__main__":
    main()
