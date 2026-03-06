import os
import yaml
from config.utils.config_loader import config_from_dict, override_config
from typing import Dict, Any, Optional
from config.utils.logging_config_database  import PitpalLoggingConfig as PLC


class LogConfigBuilder:
    def __init__(
        self,
        options
    ):
        self.default_yaml_file ="config/default/logconfig.yaml"
        self.data = self.load_config(options)

    def load_config(self, opt: dict) -> PLC:
        env_data = self._get_env()

        #Path for yaml config 
        path = opt['cfg']
        if path and os.path.exists(path):
            pass
        elif env_data['cfg'] and os.path.exists(env_data['cfg']):
            path = env_data['cfg']
        elif os.path.exists(self.default_yaml_file):
            path = self._default_yaml_file
        else:
            raise FileNotFoundError(f"No such file or directory: '{path}'")

        #set yaml  data to None.
        opt['cfg']=None
        env_data['cfg']=None
        
        with open(path) as f:
            data = yaml.safe_load(f)
        result = config_from_dict(PLC, data)
        result = override_config(result,env_data)
        result = override_config(result, opt)
        return result
    
    def _get_env(self):
        return {
                "level": os.getenv("PITPAL_LOG_LEVEL"),
                "file": os.getenv("PITPAL_LOG_FILE"),
                "cfg": os.getenv("PITPAL_LOG_YAML"),
            }
    def get(self):
        return self.data






