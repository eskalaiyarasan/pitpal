
import config.builder.cli_loader as loader
import config.builder.base_builder as bb
import config.builder.env_loader as el
from utils.oops.singleton import Singleton
from config.interface.logging_config_database import PitpalLoggingConfig as PLC
from config.interface.logging_config_database import module_name

class LoggingConfigManager(Singleton):

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.prefix=module_name
            self.args=["--logging-level","--logging-file-path","--logging-yaml"]
            self._initialized = True

    def register_arguments(self, parser):
        return loader.register_arguments(parser, self.args)
    
    def  extract_arguments(self,arg):
        return loader.extract_arguments(arg,self.prefix,self.args)

    def get_config(self, cli_args):
        env_vars = el.get_env(self.prefix)
        default_yaml = "config/default/logconfig.yaml"
        builder=bb.ConfigBuilder(cli_args,env_vars,default_yaml)
        return builder.build(PLC)

