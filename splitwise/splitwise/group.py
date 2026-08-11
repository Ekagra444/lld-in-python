from dataclasses import dataclass, field

from .user import User
from .balance_book import BalanceBook
from .expense import Expense
from .settlement_strategy import SettlementStrategy

@dataclass(slots=True)
class Group:
    id:str
    name:str
    members:set[User] = field(default_factory=set)
    expenses:list[Expense] = field(default_factory=list)
    balance_book:BalanceBook = field(default_factory=BalanceBook)

    def add_member(self,user:User)->None:
        self.members.add(user)

    def _validate_expense_membership(self,expense:Expense):
        if expense.payer not in self.members:
            raise ValueError("Payer should in the group")
        if not set(expense.participants).issubset(self.members):
            raise ValueError("Participants should be in the group")

    def add_expense(self,exp:Expense):
        self._validate_expense_membership(expense=exp)
        self.expenses.append(exp)
        self.balance_book.apply_expense(exp)
    def get_balance(self,debtor:User,creditor:User):
        return self.balance_book.get_balance(debtor=debtor,creditor=creditor)

    def get_settlement_plan(self, strategy:SettlementStrategy):
        return strategy.generate_plan(self.balance_book.get_net_balances())

    def settle(
        self,
        payer: User,
        receiver: User,
        amount: int,
    ) -> None:
        self.balance_book.settle(
            payer=payer,
            receiver=receiver,
            amount=amount,
        )