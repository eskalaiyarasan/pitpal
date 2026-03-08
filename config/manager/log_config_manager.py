
from config.builder.cli_loader as loader
import config.builder.base_builder as bb
import config.builder.env_loader as el
from utils.oops.singleton import Singleton
from config.interface.logging_config_database.py import PitpalLoggingConfig as PLC

class LoggingConfigManager(Singleton):

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.prefix="logging"     # this has to match with structure in the config.interface.looging_config_database
            self.args=["--log-level","--log-file","--log-yaml"]
            self._initialized = True

    def register_arguments(self, parser):
        return loader.register_arguments(parser, self.args)
    
    def  extract_arguments(self,arg):
        return loader.extract_arguments(arg,self.prefix,self.args)

    def get_config(cli_args):
        env_vars = el.get_env(self.prefix)
        default_yaml = "config/default/logconfig.yaml"
        builder=bb.ConfigBuilder(cli_args,env_args,default_yaml)
        return builder.build(PLC)

