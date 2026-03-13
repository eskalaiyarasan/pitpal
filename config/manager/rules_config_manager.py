###################################################
"""
easy:    no mod no time
medium:  mod 
hard:    time
=============================
PAL:   2 x 7 x 6/4
PRO:   2 x 7 x 11/5
PALM:  2 x 7' x 11/5
PLUM:  2 x 7' x 12/6
=========================
"""
###################################################
import config.builder.cli_loader as loader
import config.builder.base_builder as bb
import config.builder.env_loader as el
from utils.oops.singleton import Singleton
from config.interface.logging_config_database import PitpalLoggingConfig as PLC
from config.interface.logging_config_database import module_name

class EngineConfigManager(Singleton):

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.prefix=module_name
            self.args=["--engine-yaml","--engine-npits", "--engine-nside" , "--engine-nseeds",
                       "--engine-algo" , "--engine-capture", "--engine-direction" ,
                       , "--engine-level" ]
            self._initialized = True

    def register_arguments(self, parser):
        return loader.register_arguments(parser, self.args)
    
    def  extract_arguments(self,arg):
        return loader.extract_arguments(arg,self.prefix,self.args)

    def get_config(self, cli_args, rule=0):
        env_vars = el.get_env(self.prefix)
        default_yaml = [ "engine/rules/json/classicpal.yaml",
                         "config/default
        builder=bb.ConfigBuilder(cli_args,env_vars,default_yaml,True)
        return builder.build(PLC)

