from dataclasses import dataclass

module_name = "engine"


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
    count: int


@dataclass(frozen=True)
class PitsRuleConfig:
    nseeds: int
    npits: int
    nside: int


@dataclass(frozen=True)
class BoardRuleConfig:
    level: str
    base: PitsRuleConfig
    fruit: Fruiting
    time: TimePerMove
    clock: ClockRule
    captureplus: bool


@dataclass(frozen=True)
class EngineRuleConfig:
    algo: str
    nplayer: int
    kingzpit: bool
    capture: str
    json: str


@dataclass(frozen=True)
class RuleConfig:
    board: BoardRuleConfig
    rule: EngineRuleConfig
    yaml: str


@dataclass(frozen=True)
class PitpalRuleConfig:
    engine: RuleConfig
