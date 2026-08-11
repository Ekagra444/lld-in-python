from abc import ABC, abstractmethod

from .user import User
from .settlement_plan import SettlementPlan


class SettlementStrategy(ABC):

    @abstractmethod
    def generate_plan(
        self,
        net_balances: dict[User, int],
    ) -> SettlementPlan:
        ...