import engine.src.tier.abstracttier as abx
import engine.src.common as common
import utils.events.event as event
import utils.jsonUtils.pitpal_json_schema_utils as Jsu
import config.interface.rule_config_database as rm
import config.builder.base_builder as build
import json

class tier(abx.basetier):
    def __init__(self, config: rm.PitpalRuleConfig):
        self.json_data = self.init(config)

    def init(self, config: rm.PitpalRuleConfig):
        if config.engine.tier.strip() != "pod":
            return None
        self.jsonf = "engine/rules/json/pod.json"
        ret = super().init(config)
        if ret is not None:
            ret = build.deep_merge(self.json_data , ret)
        return ret
    def get_json(self):
        return self.json_data

        
        
        
        

        
