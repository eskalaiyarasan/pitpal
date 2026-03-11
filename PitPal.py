import argparse
import config.manager.config_manager as CM
from utils.logging.pitpal_logger import PitPalLogger
#from engine.engine import Engine



def argument_list():
    parser = argparse.ArgumentParser()
    CM.getLogConfigManager().register_arguments(parser)
    return parser.parse_args()

def init_logger(args):
    log_cli = CM.getLogConfigManager().extract_arguments(args)
    log_config = CM.getLogConfigManager().get_config(log_cli)
    print(log_config)
    PitPalLogger.initialize(log_config)


def main():
    args = argument_list()
    init_logger(args)



if __name__ == "__main__":
    main()
