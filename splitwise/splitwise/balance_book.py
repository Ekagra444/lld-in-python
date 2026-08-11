from collections import defaultdict

from .expense import Expense
from .user import User


class BalanceBook:
    def __init__(self) -> None:
        # pairwise debts
        self._debts: dict[User, dict[User, int]] = defaultdict(
            lambda: defaultdict(int)
        )

    def apply_expense(self, expense: Expense) -> None:
        payer = expense.payer

        for user, share in expense.shares.items():
            if user == payer:
                continue

            self._add_debt(
                debtor=user,
                creditor=payer,
                amount=share,
            )

    def _add_debt(
        self,
        debtor: User,
        creditor: User,
        amount: int,
    ) -> None:
        if amount <= 0:
            raise ValueError("Debt amount must be positive")

        opposite_debt = self._debts[creditor][debtor]

        if opposite_debt >= amount:
            self._debts[creditor][debtor] -= amount
        else:
            self._debts[creditor][debtor] = 0
            self._debts[debtor][creditor] += (
                amount - opposite_debt
            )

    def get_balance(
        self,
        debtor: User,
        creditor: User,
    ) -> int:
        return self._debts.get(debtor, {}).get(creditor, 0)

    def get_net_balances(self) -> dict[User, int]:
        balances: dict[User, int] = defaultdict(int)

        for debtor, creditors in self._debts.items():
            for creditor, amount in creditors.items():
                if amount == 0:
                    continue

                balances[debtor] -= amount
                balances[creditor] += amount

        return dict(balances)

    def settle(
        self,
        payer: User,
        receiver: User,
        amount: int,
    ) -> None:
        if amount <= 0:
            raise ValueError(
                "Settlement amount must be positive"
            )

        self._add_debt(
            debtor=receiver,
            creditor=payer,
            amount=amount,
        )   

        