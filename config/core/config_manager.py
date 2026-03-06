import config.core.logging_config_manager as lcm
import config.builder.base_builder as bb
import config.builder.env_loader as el

def get_logger_config(cli_args):
    env_vars = el.get_logger_env()
    default_yaml = "config/default/logconfig.yaml"
    builder=bb.ConfigBuilder(cli_args,env_args,default_yaml)
    return builder.build(lcm.PitpalLoggingConfig)
