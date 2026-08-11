import pytest
from splitwise.group import Group
from splitwise.expense import Expense
from splitwise.equal_split import EqualSplit
from splitwise.user import User
from splitwise.greedy_settlement_strategy import GreedySettlementStrategy
@pytest.fixture
def users():
    return {
        "alice": User(id="1", name="Alice"),
        "bob": User(id="2", name="Bob"),
        "charlie": User(id="3", name="Charlie"),
    }    

def test_complete_group_flow(users):
    group = Group(
        id="g1",
        name="Trip",
    )

    for user in users.values():
        group.add_member(user)

    # Alice pays ₹900.
    expense_1 = Expense(
        id="e1",
        payer=users["alice"],
        participants=[
            users["alice"],
            users["bob"],
            users["charlie"],
        ],
        amount=900,
        split_strategy=EqualSplit()
    )
    expense_2 = Expense(
        id="e2",
        payer=users["bob"],
        participants=[
            users["alice"],
            users["bob"],
            users["charlie"],
        ],
        amount=600,
        split_strategy=EqualSplit()
    )
    group.add_expense(expense_1)
    group.add_expense(expense_2)

    # Net position:
    #
    # Alice   +400
    # Bob     +100
    # Charlie -500

    net_balances = (
        group.balance_book.get_net_balances()
    )

    assert net_balances == {
        users["alice"]: 400,
        users["bob"]: 100,
        users["charlie"]: -500,
    }

    assert sum(net_balances.values()) == 0

    # Generate settlement plan.
    plan = group.get_settlement_plan(
        GreedySettlementStrategy()
    )

    assert len(plan.settlements) == 2

    # Execute the generated plan.
    for settlement in plan.settlements:
        group.settle(
            payer=settlement.payer,
            receiver=settlement.receiver,
            amount=settlement.amount,
        )

    # Everyone is now settled.
    final_balances = (
        group.balance_book.get_net_balances()
    )

    assert final_balances == {
        users["alice"]: 0,
        users["bob"]: 0,
        users["charlie"]: 0,
    }