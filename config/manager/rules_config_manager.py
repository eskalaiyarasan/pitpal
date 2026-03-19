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
import os

import yaml

import config.builder.base_builder as bb
import config.builder.cli_loader as loader
import config.builder.env_loader as el
import config.builder.yaml_loader as yl
import config.interface.rule_config_database as RCD
from config.interface.rule_config_database import module_name
from utils.logging.pitpal_logger import PitPalLogger as l
from utils.oops.singleton import Singleton


class EngineConfigManager(Singleton):
    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.prefix = module_name
            self.args = [
                "--engine-yaml",
                "--engine-rule",
                "--engine-level",
                "--engine-dir",
            ]
            self._initialized = True
            self.logger = l.get_logger()

    def register_arguments(self, parser):
        return loader.register_arguments(parser, self.args)

    def extract_arguments(self, arg):
        return loader.extract_arguments(arg, self.prefix, self.args)

    def get_config(self, cli_args, rule=0):
        env_vars = el.get_env(self.prefix)
        self.logger.debug(f"rules config manager <| {env_vars} ")
        self.logger.debug(f"rules config manager <:| {cli_args} ")
        default_yaml = "config/default/ruleconfig.yaml"
        args = bb.merge(cli_args, env_vars)
        self.logger.debug(f"rules config manager >|<| {args} ")
        default_yaml = self.derive_default_yaml(args, default_yaml)
        self.logger.debug("default_yaml:" + str(default_yaml))
        builder = bb.ConfigBuilder({}, {}, default_yaml)
        return builder.build(RCD.PitpalRuleConfig)

    def _find_engine_config(self, input_name, directory="config/system/engine/"):
        self.logger.info(f"_find_engine_config :: {input_name}")

        # Check if directory exists to avoid errors
        if not os.path.exists(directory):
            return None

        # Loop through each file in the directory
        for filename in os.listdir(directory):
            # Process only .yaml or .yml files
            if filename.endswith(".yaml"):
                filepath = os.path.join(directory, filename)

                try:
                    with open(filepath, "r") as file:
                        content = yaml.safe_load(file)

                        # Ensure content is a valid dictionary before checking keys
                        if isinstance(content, dict):
                            # Extract values and compare against your criteria
                            status = content.get("status")
                            tier = content.get("tier")
                            name = content.get("name")
                            clean_name = (
                                str(name).replace("\r", "").replace("\n", "").strip()
                            )
                            clean_input = (
                                str(input_name)
                                .replace("\r", "")
                                .replace("\n", "")
                                .strip()
                                .strip(":")
                                .strip()
                            )

                            # if ("OK" in str(status).strip()
                            #     and int(str(tier)) == 1
                            #     and clean_name == clean_input
                            # ):
                            if clean_name == clean_input:
                                self.logger.debug(
                                    f"rules config manager <::> suscess found for the rules {filename} "
                                )
                                return os.path.join(directory, filename)
                            else:
                                self.logger.debug(
                                    f"rules config manager <::> no match {filename} : {clean_name} == {clean_input}"
                                )

                except (yaml.YAMLError, IOError):
                    # Skip files that are not valid YAML or cannot be read
                    self.logger.error(
                        "rules config manager : not a valid yaml file " + str(filepath)
                    )
                    continue

        # Return None if no matching file is found after the loop
        return None

    def derive_default_yaml(self, args, default_yaml):
        engine_yaml = None
        directory = "config/system/engine/"
        try:
            if args["engine.dir"] is not None:
                directory = args["engine.dir"]
                self.logger.info(
                    f"rules config manager :: engine base directory -> {directory}"
                )
        except Exception as e:
            self.logger.error("derive_default_yaml: " + str(args))
            self.logger.error(f"Failed: {e}")

        try:
            param = "engine.yaml"

            if param in args and args[param] is not None:
                engine_yaml = args[param]
            elif args["engine.rule"] is not None:
                engine_yaml = self._find_engine_config(args["engine.rule"], directory)
            else:
                self.logger.error(
                    "rules config manager : not able to find rules, switch to default"
                )
        except Exception as e:
            self.logger.error("derive_default_yaml: " + str(args))
            self.logger.error(f"Failed: {e}")

        engine_yaml_data = None
        if engine_yaml is not None and os.path.exists(engine_yaml):
            try:
                with open(engine_yaml, "r") as file:
                    engine_yaml_data = yaml.safe_load(file)
            except Exception as e:
                self.logger.error(
                    f"rules_config_manager:: {e} :: file : {engine_yaml} "
                )
        else:
            self.logger.error(
                f"rules config manager:: {engine_yaml} yaml file not found"
            )
        default_yaml_data = None
        with open(default_yaml, "r") as file:
            default_yaml_data = yaml.safe_load(file)
        if engine_yaml_data:
            overrides = bb.deep_merge(
                engine_yaml_data["rule"], default_yaml_data[self.prefix]["rule"]
            )
            default_yaml_data[self.prefix]["rule"] = overrides
            if (
                "engine.level" not in args
                or args["engine.level"] not in engine_yaml_data["options"]
            ):
                args["engine.level"] = engine_yaml_data["options"][0]
                self.logger.error(
                    "rules config manager :level is not found switch to default"
                )
            changes = engine_yaml_data[args["engine.level"]]
            overrides = bb.deep_merge(changes, default_yaml_data[self.prefix]["board"])
            default_yaml_data[self.prefix]["board"] = overrides
        else:
            self.logger.error(
                "rules config manager ??: config not found switch to default"
            )
        return yl.write_to_temp(default_yaml_data, self.prefix)
