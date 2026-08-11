from dataclasses import dataclass, field

from .settlement import Settlement

@dataclass(frozen=True, slots=True)
class SettlementPlan:
    settlements:list[Settlement]= field(default_factory=list)