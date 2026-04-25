from dataclasses import dataclass
from typing import List

module_name="engine"

PitRule = List[int]
@dataclass(frozen=True)
class TimePerMove:
    max: int
    enabled: bool 


@dataclass(frozen=True)
class ClockRule:
    enabled: bool
    min: int


@dataclass(frozen=True)
class BaseRule:
    nseeds: int
    npits: int
    nside: int

@dataclass(frozen=True)
class DetailRuleConfig:
    base: BaseRule
    fruit: int
    time: TimePerMove
    clock: ClockRule
    specialPits: PitRule

@dataclass(frozen = True)
class MinMaxPlayers:
    min: int
    max: int 

@dataclass(frozen=True)
class RuleConfig:
    level: str
    mode: str
    tier: str
    json: str
    algo: str
    players:MinMaxPlayers
    details: DetailRuleConfig
    yaml: str

@dataclass(frozen=True)
class PitpalRuleConfig:
    engine: RuleConfig
