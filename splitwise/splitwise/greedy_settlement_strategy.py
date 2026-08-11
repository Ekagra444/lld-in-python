import heapq

from .user import User
from .settlement import Settlement
from .settlement_plan import SettlementPlan
from .settlement_strategy import SettlementStrategy

class GreedySettlementStrategy(SettlementStrategy):

    def generate_plan(
        self,
        net_balances: dict[User, int],
    ) -> SettlementPlan:
        creditors: list[tuple[int, str , User]] = []
        debtors: list[tuple[int, str , User]] = []

        for user, balance in net_balances.items():

            if balance > 0:
                heapq.heappush(creditors,(-balance,user.id,user))
            else:
                heapq.heappush(debtors,(balance,user.id,user))
        settlements:list[Settlement] = []
        while creditors and debtors:
            creditor_amount, _ , creditor = heapq.heappop(
                creditors
            )

            debtor_amount, _ , debtor = heapq.heappop(
                debtors
            )
            creditor_amount = -creditor_amount
            debtor_amount = -debtor_amount

            amount = min(
                creditor_amount,
                debtor_amount,
            )

            settlements.append(
                Settlement(
                    payer=debtor,
                    receiver=creditor,
                    amount=amount,
                )
            )

            creditor_remaining = (
                creditor_amount - amount
            )

            debtor_remaining = (
                debtor_amount - amount
            )

            if creditor_remaining > 0:
                heapq.heappush(
                    creditors,
                    (-creditor_remaining, creditor.id, creditor),
                )

            if debtor_remaining > 0:
                heapq.heappush(
                    debtors,
                    (-debtor_remaining,debtor.id, debtor),
                )

        return SettlementPlan(
            settlements=settlements
        )