import pytest
from splitwise.user import User
from splitwise.equal_split import EqualSplit
from splitwise.expense import Expense
from splitwise.balance_book import BalanceBook
from splitwise.greedy_settlement_strategy import GreedySettlementStrategy
from splitwise.settlement_strategy import SettlementStrategy
from splitwise.settlement_plan import SettlementPlan
def test_plan():
    alice = User("1", "Alice")
    bob = User("2", "Bob")
    charlie = User("3", "Charlie")

    expense = Expense(
        id="e1",
        payer=alice,
        amount=1500,
        participants=[alice, bob, charlie],
        split_strategy=EqualSplit(),
    )

    book = BalanceBook()
    book.apply_expense(expense)
    expense2 = Expense(
        id="e1",
        payer=charlie,
        amount=300,
        participants=[alice, bob, charlie],
        split_strategy=EqualSplit(),
    )
    book.apply_expense(expense2)

    net_balances:dict[User,int] = book.get_net_balances()
    settlement_strategy:SettlementStrategy = GreedySettlementStrategy()
    settlement_plan:SettlementPlan = settlement_strategy.generate_plan(net_balances=net_balances)
    settlement1 = settlement_plan.settlements[0]
    assert settlement1.payer == bob
    settlement1.receiver == alice
    settlement1.amount == 600

    settlement2 = settlement_plan.settlements[1]
    assert settlement2.payer == charlie
    settlement2.receiver == alice
    settlement2.amount == 300

    



    


