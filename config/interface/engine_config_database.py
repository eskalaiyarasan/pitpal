from dataclasses import dataclass

module_name="rule"

@dataclass(frozen=True)
class TimePerMove:
    max: int
    enabled: bool 


@dataclass(frozen=True)
class ClockRule:
    enabled: bool
    min: int


@dataclass(frozen=True)
class Fruiting:
    dormant: bool
    period: int

@dataclass(frozen=True)
class BoardConfig:
    nseeds: int
    npits: int
    nside: int

@dataclass(frozen=True)
class VarRuleConfig:
    board: BoardConfig
    fruit: Fruiting
    time: TimePerMove
    clock: ClockRule
    kingzpit: bool
    capture: str
    captureplus: bool 


@dataclass(frozen=True)
class FixedRuleConfig:
    level: str
    algo: str 
    engine:str 


@dataclass(frozen=True)
class RuleConfig:
    var: VarRuleConfig
    fixed: FixedRuleConfig
    yaml: str

@dataclass(frozen=True)
class PitpalRuleConfig:
    rule: RuleConfig
